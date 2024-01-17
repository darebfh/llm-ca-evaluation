from openai import OpenAI
import constants

from evaluation.llm_client import LLMClient
from evaluation.utility.vertical_list_output_parser import VerticalListOutputParser


class OpenAIClient(LLMClient):
    def __init__(self):
        super().__init__()
        # key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI()
        self.parser = VerticalListOutputParser()

    def send_data_to_api(self, data, role):
        # Implement the logic to send data to the API
        # You may want to loop through the data and send it line by line
        print("Role: ", role)
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": role["description"] + constants.TASK,
                },
                {
                    "role": "user",
                    "content": role["example_question"],
                },
                {"role": "assistant", "content": role["example_answer"]},
                {
                    "role": "user",
                    "content": data,
                },
            ],
        )
        print("output: " + completion.choices[0].message.content)
        output = completion.choices[0].message.content
        parsed_output = self.parser.parse(output)
        print("parsed output: " + str(parsed_output))
        return parsed_output
