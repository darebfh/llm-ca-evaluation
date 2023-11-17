import os

from openai import OpenAI
import constants
from dotenv import load_dotenv, find_dotenv

from evaluation.llm_client import LLMClient


class OpenAIClient(LLMClient):
    def __init__(self):
        super().__init__()
        key = os.getenv("OPENAI_API_KEY")
        print(key)
        self.client = OpenAI(api_key=key)

    def send_data_to_api(self, data):
        # Implement the logic to send data to the API
        # You may want to loop through the data and send it line by line

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist eine Patientin bzw. ein Patient und lernst erst seit zwei Monaten Deutsch. Deswegen verfügst du nur über einen Basis-Wortschatz. Dir steht eine Mammographie bevor. Definiere in dem Ausmass, in dem es deine Deutschkenntnisse erlauben, zehn verschiedene Formulierungen einer Frage zur genannten Antwort. Deine Antwort ist eine .csv Datei mit den Spalten «antwort» und «frage». Die Spalte «antwort» bleibt dabei immer gleich und enthält die vorgegebene Antwort. ",
                },
                {
                    "role": "user",
                    "content": "Für die Mammografie ist keine spezielle Vorbereitung notwendig. Möglicherweise Entfernung von Schmuck im Brustbereich.",
                },
            ],
        )
        print(completion)
        return completion
