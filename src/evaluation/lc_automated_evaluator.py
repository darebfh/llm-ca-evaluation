from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv, find_dotenv

from evaluation.vertical_list_output_parser import VerticalListOutputParser


class LangChainAutomatedEvaluator:
    def __init__(self, roles=None, model="gpt-3.5-turbo"):
        load_dotenv(find_dotenv())
        self.model = model
        self.roles = roles

    def evaluate(self, question):
        if self.roles is None or len(self.roles) == 0:
            raise Exception("No roles given")
        result = {}

        task = (
            "Definiere anhand folgender Antwort zehn möglichst unterschiedliche Versionen einer Frage. Passe deine "
            "Wortwahl an deine Gesundheitskompetenz und deine Sprachniveau an. Gib jeweils nur die Formulierung "
            "getrennt durch einen Zeilenumbruch (\n) zurück."
        )

        for key, value in self.roles.items():
            chain = self.create_chain(value, task)
            output = chain.invoke({"text": question})
            result[key] = output

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
