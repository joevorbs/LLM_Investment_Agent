# LLM Investment Agent
A tool to aggregate all personal investment account information and use an LLM query layer to answer questions on said investments. This is for fun to learn more about LLMs/GenAi and how to intergrate with them data pipelines.

The goal is to pull data from each brokerage, aggregate it, store it, then apply an LLM over it to answer questions and get updates on my accounts.

This pipeline will be AWS based and will leverage the Plaid API to pull the data.

The architecture will look something like this:
- Secrets Manager to store API keys + any associated brokerage information
- Lambda to make the API call and aggregate the data (would switch to glue for the processing if the data was that big but highly doubt it)
- Dynamo to store the data
- Lambda for the bedrock and query layer

Front end / chat bot style interface will come later. Maybe will integrate dashboards with Quicksight but that will be phase 2.

For the access keys to Plaid (currently sandbox - still stored in secrets manager):
  1. Made a post request at: https://sandbox.plaid.com/sandbox/public_token/create
  2. Took the body of the request and passed in at: https://sandbox.plaid.com/item/public_token/exchange
