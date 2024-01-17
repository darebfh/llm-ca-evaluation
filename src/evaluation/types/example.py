class Example:
    def __init__(
        self, identifier, question, answer, qa_data=None, alternative_questions=None
    ):
        if alternative_questions is None:
            alternative_questions = {}
        self.identifier = identifier
        self.question = question
        self.answer = answer
        self.alternative_questions = alternative_questions
        self.qa_data = {}

    def __json__(self):
        return {
            "identifier": self.identifier,
            "question": self.question,
            "answer": self.answer,
            "alternative_questions": self.alternative_questions,
            "qa_data": self.qa_data,
        }
