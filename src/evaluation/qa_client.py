import requests


class QAClient:
    def __init__(self, url):
        self.url = url

    def get_answer(self, question):
        print("Sending question to QA endpoint: " + question)
        response = requests.post(self.url, json={"text": question})
        if response.ok:
            json_response = response.json()
            qa_answer = json_response["result"]
        else:
            qa_answer = str(response.status_code)
        print("Received answer from QA endpoint: " + qa_answer)
        return qa_answer
