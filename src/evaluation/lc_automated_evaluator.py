import datetime
import json

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv, find_dotenv

import constants
from evaluation.utility.vertical_list_output_parser import VerticalListOutputParser


class LangChainAutomatedEvaluator:
    def __init__(self, roles=None, model="gpt-3.5-turbo"):
        load_dotenv(find_dotenv())
        self.model = model
        self.roles = roles

    def get_alternative_questions(self, input):
        if self.roles is None or len(self.roles) == 0:
            raise Exception("No roles given")
        result = {}

        task = constants.TASK

        for key, value in self.roles.items():
            print("Running automated test for role: " + key)
            chain = self.create_chain(value, task)
            print("Input: " + input)
            output = chain.invoke({"text": input})
            print("Output: " + json.dumps(output, ensure_ascii=False))
            result[key] = output
        result["created_with"] = self.model
        result["created_at"] = datetime.datetime.now().isoformat()
        print("Result: " + json.dumps(result, ensure_ascii=False))
        return result

    def create_chain(self, role, task):
        template = role + task
        human_template = "{text}"

        chat_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", template),
                ("human", human_template),
            ]
        )
        # chat_prompt.save(role + "_chat_prompt.json") not implemented (yet)
        chain = chat_prompt | ChatOpenAI(model=self.model) | VerticalListOutputParser()
        return chain
