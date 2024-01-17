import datetime
import os

import constants
import openai_client
from dotenv import load_dotenv, find_dotenv

from evaluation import qa_client
from evaluation.utility import json_handler, csv_handler
import json


class Evaluator:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.openai_client = openai_client.OpenAIClient()
        self.qa_client = qa_client.QAClient(constants.QA_ENDPOINT)
        self.csv_handler = csv_handler.CSVHandler()
        self.json_handler = json_handler.JsonHandler()
        self.roles = constants.ROLES
        self.examples = []

        if os.getenv("TEST") == "True":
            # Question variations already generated, loading from files
            self.examples = self.json_handler.load_generated_variations()
            print("Loaded " + str(len(self.examples)) + " examples")
            print(self.examples)
        else:
            # Load examples from CSV
            self.examples = self.csv_handler.read_csv(constants.QAP_DEFINITIONS_FILE)
            # Generate question variations

            if constants.QAP_LIMIT:
                print(
                    "TEST MODE - Limiting examples to "
                    + str(constants.QAP_LIMIT)
                    + " examples"
                )
                self.examples = self.examples[
                    constants.QAP_LIMIT[0] : constants.QAP_LIMIT[1]
                ]
            self.get_question_variations_for_all_qaps()

    def get_question_variations_for_all_qaps(self):
        for example in self.examples:
            question = example.question
            print("Generating variations for question: " + question)
            alternative_questions = self.get_question_variations_for_qap(question)
            example.alternative_questions = alternative_questions
            example.variations_created_at = datetime.datetime.now().isoformat()
            self.save_object(
                example, constants.QAP_VARIATIONS_OUTPUT_FOLDER + example.identifier
            )
            input("Press Enter to continue...")

    def get_question_variations_for_qap(self, question):
        result = {}
        for role_name, role_details in self.roles.items():
            print("Getting questions for role: " + role_name)
            result[role_name] = self.openai_client.send_data_to_api(
                question, role_details
            )
        return result

    def get_qa_response_for_all_variations(self):
        for example in self.examples:
            for role, questions in example.alternative_questions.items():
                example.qa_data[role] = {}
                for question in questions:
                    answer = self.qa_client.get_answer(question)
                    example.qa_data[role][question] = answer
                self.save_object(
                    example,
                    constants.QA_ANSWERS_OUTPUT_FOLDER + example.identifier,
                )

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
        return correct_answers, incorrect_answers

    @staticmethod
    def save_object(obj, full_path):
        print(json.dumps(obj, ensure_ascii=False, default=lambda o: o.__dict__))
        with open(full_path + ".json", "w") as outfile:
            json.dump(obj, outfile, ensure_ascii=False, default=lambda o: o.__dict__)


if __name__ == "__main__":
    evaluator = Evaluator()
    evaluator.get_qa_response_for_all_variations()
    evaluator.compute_metrics()
