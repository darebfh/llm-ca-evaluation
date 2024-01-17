import os

import constants
import openai_client
from dotenv import load_dotenv, find_dotenv

from evaluation import qa_client
from evaluation.utility import json_handler, csv_handler
from lc_automated_evaluator import LangChainAutomatedEvaluator
import json


class Evaluator:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.qa_client = qa_client.QAClient(constants.QA_ENDPOINT)
        self.csv_handler = csv_handler.CSVHandler()
        self.json_handler = json_handler.JsonHandler()
        self.roles = constants.ROLES
        self.examples = []

    def run_automated_test_lc(self):
        for example in self.examples:
            answer = example.answer
            print("Running automated test for answer: " + answer)
            alternative_questions = self.run_langchain_test(answer)
            example.alternative_questions = alternative_questions
            self.save_object(example, example.identifier)

    def run_automated_test_openai(self):
        for example in self.examples:
            answer = example.answer
            print("Running automated test for answer: " + answer)
            alternative_questions = self.run_openai_test(answer)
            example.alternative_questions = alternative_questions
            print(example)
            # example["created_at"] = datetime.datetime.now().isoformat()
            self.save_object(example, example.identifier)
        self.get_qa_response()

    def get_qa_response(self):
        for example in self.examples:
            for role, questions in example.alternative_questions.items():
                example.qa_data[role] = {}
                for question in questions:
                    answer = self.qa_client.get_answer(question)
                    example.qa_data[role][question] = answer
                self.save_object(example, example.identifier + "_qa")

    def run_langchain_test(self, answer):
        langchain = LangChainAutomatedEvaluator(roles=self.roles)
        results = langchain.get_alternative_questions(answer)
        return results

    def run_openai_test(self, answer):
        openai = openai_client.OpenAIClient()
        result = {}
        print("Getting questions for answer: " + answer)
        for role in self.roles:
            print("Getting questions for role: " + role)
            result[role] = openai.send_data_to_api(answer, role)
        return result

    def compute_metrics(self):
        for example in self.examples:
            self.compute_metrics_for_example(example)

    def compute_metrics_for_example(self, example):
        for role in self.roles:
            self.compute_metrics_for_role(example, role)

    def compute_metrics_for_role(self, example, role):
        correct_answers = 0
        incorrect_answers = 0
        for question, answer in example.qa_data[role].items():
            if answer == example.answer:
                correct_answers += 1
            else:
                incorrect_answers += 1

    @staticmethod
    def save_object(obj, filename):
        print(json.dumps(obj, ensure_ascii=False, default=lambda o: o.__dict__))
        with open("data/output/" + filename + ".json", "w") as outfile:
            json.dump(obj, outfile, ensure_ascii=False, default=lambda o: o.__dict__)


if __name__ == "__main__":
    evaluator = Evaluator()
    if os.getenv("TEST") == "True":
        print(
            "TEST MODE - Limiting examples to "
            + str(constants.TEST_LIMIT)
            + " examples"
        )
        evaluator.examples = evaluator.json_handler.load_examples_from_folder()
        print("Loaded " + str(len(evaluator.examples)) + " examples")
        print(evaluator.examples)
    else:
        evaluator.examples = evaluator.examples[: constants.TEST_LIMIT]
        evaluator.run_automated_test_openai()
    evaluator.get_qa_response()
    evaluator.compute_metrics()
