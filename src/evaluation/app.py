import datetime
import os

import constants
from evaluation import openai_client
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

        if os.getenv("GET_VARIANTS") == "False":
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
            # input("Press Enter to continue...")

    def get_question_variations_for_qap(self, question):
        result = {}
        for role_name, role_details in self.roles.items():
            print("Getting questions for role: " + role_name)
            result[
                role_name
            ] = self.openai_client.generate_question_variations_for_role(
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

    def get_new_questions_for_domain(self):
        new_questions = {}
        for role_name, role_details in self.roles.items():
            result = self.openai_client.generate_new_questions_for_role(role_details)
            new_questions[role_name] = result
        self.save_object(
            new_questions,
            constants.NEW_QUESTIONS_OUTPUT_FOLDER + datetime.datetime.now().isoformat(),
        )
        new_qaps = []
        for role, questions in new_questions.items():
            for question in questions:
                answer = self.qa_client.get_answer(question)
                new_qaps.append((question, answer))
        filepath = (
            constants.NEW_QUESTIONS_OUTPUT_FOLDER
            + datetime.datetime.now().isoformat()
            + ".csv"
        )
        self.csv_handler.write_to_csv(filepath, new_qaps, ["question", "answer"])

    def compute_metrics(self):
        example_results = {
            "results_all_examples": {},
            "correct_answers_total": 0,
            "correct_answers_total_per_role": {},
            "incorrect_answers_total": 0,
            "variation_too_short_total": 0,
            "no_answer_found_total": 0,
        }

        for example in self.examples:
            result = self.compute_metrics_for_example(example)
            example_results["results_all_examples"][example.identifier] = result
            example_results["correct_answers_total"] += result[
                "qap_correct_answers_total"
            ]
            example_results["incorrect_answers_total"] += result[
                "qap_incorrect_answers_total"
            ]
            example_results["variation_too_short_total"] += result[
                "qap_variation_too_short"
            ]
            example_results["no_answer_found_total"] += result["qap_no_answer_found"]
            for role, correct_answers in result[
                "qap_correct_answers_total_per_role"
            ].items():
                if role not in example_results["correct_answers_total_per_role"]:
                    example_results["correct_answers_total_per_role"][role] = 0
                example_results["correct_answers_total_per_role"][
                    role
                ] += correct_answers
        filename = (
            constants.EVALUATION_RESULTS_OUTPUT_FOLDER
            + "evaluation_results"
            + datetime.datetime.now().isoformat()
        )
        self.save_object(example_results, filename)

    def compute_metrics_for_example(self, example):
        example_result = {
            "qap_results_all_roles": {},
            "qap_correct_answers_total": 0,
            "qap_correct_answers_total_per_role": {},
            "qap_incorrect_answers_total": 0,
            "qap_variation_too_short": 0,
            "qap_no_answer_found": 0,
        }

        for role in self.roles:
            result = self.compute_metrics_for_role(example, role)
            example_result["qap_results_all_roles"][role] = result
            example_result["qap_correct_answers_total"] += result[
                "role_correct_answers"
            ]
            example_result["qap_incorrect_answers_total"] += result[
                "role_incorrect_answers_total"
            ]
            example_result["qap_variation_too_short"] += result[
                "role_variation_too_short"
            ]
            example_result["qap_no_answer_found"] += result["role_no_answer_found"]
            example_result["qap_correct_answers_total_per_role"][role] = result[
                "role_correct_answers"
            ]
        example.metrics = example_result
        return example_result

    def compute_metrics_for_role(self, example, role):
        role_result = {
            "role_correct_answers": 0,
            "role_variation_too_short": 0,
            "role_no_answer_found": 0,
            "role_incorrect_answers_total": 0,
        }
        for question, answer in example.qa_data[role].items():
            if answer == example.answer:
                role_result["role_correct_answers"] += 1
            elif answer == "400":
                role_result["role_variation_too_short"] += 1
                role_result["role_incorrect_answers_total"] += 1
            elif answer == "500":
                role_result["role_no_answer_found"] += 1
                role_result["role_incorrect_answers_total"] += 1
            else:
                role_result["role_incorrect_answers_total"] += 1
        return role_result

    @staticmethod
    def save_object(obj, full_path):
        print(json.dumps(obj, ensure_ascii=False, default=lambda o: o.__dict__))
        with open(full_path + ".json", "w") as outfile:
            json.dump(obj, outfile, ensure_ascii=False, default=lambda o: o.__dict__)


if __name__ == "__main__":
    evaluator = Evaluator()
    if os.getenv("GET_ANSWERS") == "True":
        print("Getting answers for all variations")
        evaluator.get_qa_response_for_all_variations()
    if os.getenv("EVALUATE") == "True":
        print("Evaluating results")
        evaluator.compute_metrics()
    if os.getenv("GEN_NEW_QUESTIONS") == "True":
        print("Generating new questions")
        evaluator.get_new_questions_for_domain()


def generate_new_questions():
    evaluator = Evaluator()
    evaluator.get_new_questions_for_domain()
