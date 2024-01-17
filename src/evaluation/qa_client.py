import requests


class QAClient:
    def __init__(self, url):
        self.url = url

    def get_answer(self, question):
        print("Sending question to QA endpoint: " + question)
        response = requests.post(self.url, json={"text": question})
        json_response = response.json()
        # TODO: Handle errors
        qa_answer = json_response["result"]
        print("Received answer from QA endpoint: " + qa_answer)
        return qa_answer
