# Evaluation tool for (semi-)automated evaluation of medical conversational agents

## Set-up
- Clone this repository
- Install pdm: https://github.com/pdm-project/pdm
- Run `pdm install` in the root directory of this repository


## Usage 
- Place the .csv file called "qa_content.csv" containing the questions and answers into ./data/input/
- Create an OpenAI account and get an API key. More information to be found here: https://platform.openai.com/docs/overview
- Create a file ./src/.env and specify your OpenAI API key. The file should look like this:
```OPENAI_API_KEY=<your_api_key>```
- Run 'pdm run evaluate' to start the evaluation tool
- The output will be saved to ./data/output/

WIP: Explain fully automated and semi-automated evaluation.


