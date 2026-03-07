# NBA Statistics Agent
This is a small project to get more familiar with LLMs and AWS Bedrock.
I will be obtaining NBA players' per game statistics over each year and storing them for an LLM to be able to answer questions about. Relatively simple chatbot for more exposure to the service and GenAI.
This will all be done on AWS. The data is sourced from Basketball Reference.

# Architecture (AWS)
- Glue for ETL
- DynamoDB for storage
- Bedrock & Lambda for query layer
- S3 (For hosting static webpage)
- API Gateway to pass questions to webpage
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
**"Who has the highest average 3P%?"**

---

## Lambda Output
<img width="1331" height="583" alt="Screenshot 2026-03-07 at 4 37 17 PM" src="https://github.com/user-attachments/assets/1969ddfd-14f7-47dd-8bdc-37e2951db638" />

---

## DynamoDB View
<img width="1192" height="669" alt="image" src="https://github.com/user-attachments/assets/0c8adb66-cbf0-44b3-a731-2e270f71ef93" />
