class Result:
    def __init__(self, identifier, question, answer, alternative_questions=None):
        self.identifier = identifier
        self.question = question
        self.answer = answer
        self.alternative_questions = alternative_questions

    def __json__(self):
        return {
            "field1": self.identifier,
            "field2": self.question,
            "field3": self.answer,
            "field4": self.alternative_questions,
        }
