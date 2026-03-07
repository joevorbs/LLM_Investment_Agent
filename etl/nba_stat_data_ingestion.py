import pandas as pd
import boto3
from decimal import Decimal

#Initialize boto3 + dynamodb
dynamodb = boto3.resource("dynamodb")
llm_table = dynamodb.Table("nba_stats_llm_database")

#Read in the list of nba players who we will be retrieving statistics on from basketball reference
player_table = pd.read_csv("s3://nba-stats-llm-agent/nba_player_urls.csv")

#Data Cleansing Function - loop through the players we want to get stats on from the website, then insert the data into dynamodb
def stats_cleansing_func(player_df: pd.DataFrame) -> pd.DataFrame:
    
    #Zip the first two cols of the player table df to to be able to iterate through - always pull the first two columns in the table
    player_list = list(zip(player_df.iloc[:, 0], player_df.iloc[:, 1]))

    #Loop through the players we want to get stats on from the website, then insert the data into dynamodb
    for player, slug in player_list:
        print(f"Getting per game statics for {player}")
        
        #Lower case all names and replace the space between first and last name - will be used in dynamodb to build the pk
        player_clean = player.lower().replace(" ", "_")
        
        #Basketball reference uses the first 5 characters of the players last name plus the first two letters of their first name then the numbers 01 - ex: duncati01 (Tim Duncan)
        url = f"https://www.basketball-reference.com/players/{slug}"
        #The 1 index indicates the second table on the page - a player's per game stats
        stats = pd.read_html(url)[1]
        
        #Format the table - lowercase table col names and replace any NaNs with null
        stats_clean = stats.rename(columns = str.lower)
        stats_clean = stats_clean.where(pd.notnull(stats_clean), None)
        #Remove rows that players did not play which are entirely null
        stats_clean = stats_clean.dropna(how = 'all')
        
        #Remove secondary summary table at bottom of per game table - "Yrs" and "Awards" are both the values that act as headers in the secondary table
        row_idx_match = (stats_clean.eq("Awards").any(axis = 1) | stats_clean["season"].astype(str).str.contains("Yrs", na = False))
        row_to_match = stats_clean.index[row_idx_match]
        if len(row_to_match) > 0:
            stats_clean = stats_clean.loc[:row_to_match[0]-1]
        
        #Add the pk column to the dataframe
        stats_clean['player'] = player_clean
        
        #Cast floats to decimal for the db
        stats_final = stats_clean
        float_cols = stats_final.select_dtypes(include = "float").columns
        stats_final[float_cols] = stats_clean[float_cols].applymap(lambda x: Decimal(str(x)) if pd.notnull(x) else None)
        
        #Write final df to dynamo
        write_to_dynamo(stats_final)
        
def write_to_dynamo(cleaned_player_df: pd.DataFrame):
    #Convert dataframe to dict for writing
    table_rows = cleaned_player_df.to_dict(orient = "records")
    #Write rows to dynamodb
    with llm_table.batch_writer() as batch:
        for row in table_rows:
            row["PK"] = row['player']
            row["SK"] = f"{row['season']}#TEAM#{row['team']}" #If a player got traded mid season then a second row generates with the same season so need to make it unique for this case
            #Sanity checking keys
            print(row["PK"], row["SK"])
            batch.put_item(Item = row)

#Main function
def main():
    stats_cleansing_func(player_table)

#Run the pipeline
main()
