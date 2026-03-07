import json
import boto3

#Initialize bedrock
bedrock = boto3.client("bedrock-runtime")
bedrock_model = "amazon.nova-lite-v1:0"
#Initialize dynamodb
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("nba_stats_llm_database")
#Get dynamodb table items for llm to access
items = table.scan()['Items']

def lambda_handler(event, context):

    prompt = f"""
    You are an NBA expert answering questions about NBA players and statistics. The data you need to analyze is stored in a dynamodb table.

    The database records are {json.dumps(items, default = str)}



    Rules:
    - When returning a player's name, remove the _ character, replace it with a space, and title case their name
    - Return ONLY the final answer WITH the associated statistics
    - Don't show reasoning
    - Don't explain the steps
    - Do not use LaTeX formatting
    - Do not wrap numbers in $ symbols
    - Use plain text only
    - If a question is asked about a player that does not exist please return the message "This player is not in the database. The available players are: " then list all players in the database.
    - Answer concisely and directly

    Question: {event['question']}
    
    """
    
    #Call the bedrock model
    model_response = bedrock.invoke_model(
        modelId = bedrock_model,
        body = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 150,
                "temperature": 0,
                "topP": 0,
                "topK": 1
            }
        })
    )

    body = json.loads(model_response["body"].read())
    output = body["output"]["message"]["content"][0]["text"]

    return output
