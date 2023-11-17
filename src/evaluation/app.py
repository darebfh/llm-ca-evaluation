import openai_client
import csv_handler
from dotenv import load_dotenv, find_dotenv
from lc_automated_evaluator import LangChainAutomatedEvaluator
import json


class Evaluator:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.api_client = openai_client.OpenAIClient()
        self.csv_handler = csv_handler.CSVHandler()
        self.questions_answers = self.csv_handler.read_csv("data/input/qa_content.csv")
        self.roles = {  # TODO: Read from file
            "high_literacy": "Du bist eine gebildete Patientin bzw. ein Patient mit hoher Gesundheitskompetenz. Dir "
            "steht eine Mammographie bevor.",
            "low_literacy": "Du bist eine Patientin bzw. ein Patient mit geringer Gesundheitskompetenz und kennst "
            "dich im Gesundheitswesen kaum aus. Dir steht eine Mammographie bevor.",
            "poor_german": "Du bist eine Patientin bzw. ein Patient und lernst erst seit ein wenigen Wochen Deutsch. "
            "Deine Deutschkentnisse sind deswegen noch sehr gering. Dir steht eine Mammographie bevor.",
        }

    def run_automated_test(self):
        for line in self.questions_answers:
            answer = line[2]
            completions = self.api_client.send_data_to_api(answer)
            questions = [completion.choices[0].text for completion in completions]
            self.csv_handler.write_to_csv("data/output/qa_content.csv", completions)

    def run_semi_automated_test(self):
        for line in self.questions_answers:
            print("foo")

    def run_langchain_test(self):
        langchain = LangChainAutomatedEvaluator(roles=self.roles)
        results = langchain.evaluate(
            "Für die Mammografie ist keine spezielle Vorbereitung notwendig. Möglicherweise Entfernung von Schmuck im Brustbereich."
        )
        self.save_results(results)

    @staticmethod
    def save_results(results):
        print(json.dumps(results, ensure_ascii=False))
        with open("data/output/langchain_results.json", "w") as outfile:
            json.dump(results, outfile, ensure_ascii=False)


if __name__ == "__main__":
    evaluator = Evaluator()
    # evaluator.run_automated_test()
    evaluator.run_langchain_test()
