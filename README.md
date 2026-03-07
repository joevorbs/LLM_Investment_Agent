# NBA Statistics Agent
This is a small project to get more familiar with LLMs and AWS Bedrock.
I will be obtaining NBA players' per game statistics over each year and storing them for an LLM to be able to answer questions about. Relatively simple chatbot for more exposure to the service and GenAI.
This will all be done on AWS. The data is sourced from Basketball Reference.

# Architecture (AWS)
- Glue for ETL
- DynamoDB for storage
- Bedrock & Lambda for query layer (Also using the bedrock lambda to expose to the webpage)
- S3 (For hosting static webpage)
- HTML / Python (Plotly) for charting and webpage
- Terraform for IAC and deployment

# Phase 1
## ETL & Query Layer
- Read NBA player statistics data in from Basketball Reference
- Write data to database
- Apply LLM query layer over the database

# Phase 2
- Allow the agent to pull the data for us without specifying what we want upfront
- Create basic front end
- Ask the questions / get responses on the webpage and generate charts based on the question

- # Phase 3
- IAC

# Sample (Current State)

## Question
**"Show me a chart of LeBron James PPG per year"**

---

## Lambda Output on Webpage
<img width="858" height="548" alt="image" src="https://github.com/user-attachments/assets/1271d385-258e-45eb-b93b-1ddc7d750da4" />

---

## DynamoDB View
<img width="1192" height="669" alt="image" src="https://github.com/user-attachments/assets/0c8adb66-cbf0-44b3-a731-2e270f71ef93" />
