# NBA Statistics Agent
This is a small project to get more familiar with LLMs and AWS Bedrock.
I will be obtaining NBA players' per game statistics over each year and storing them for an LLM to be able to answer questions about. Relatively simple chatbot for more exposure to the service and GenAI.
This will all be done on AWS. The data is sourced from Basketball Reference.

# Architecture (AWS)
- Glue for ETL
- DynamoDB for storage
- Bedrock / Lambda for query layer
- Quicksight for visualization
- Terraform for IAC and deployment (why not)

# Phase 1
## ETL & Query Layer
- Read NBA player statistics data in from Basketball Reference
- Write data to database
- Apply LLM query layer over the database

# Phase 2
- Create basic front end
- Connect AWS Quicksight to the database and use the agent to create dashboards based on the question asked
