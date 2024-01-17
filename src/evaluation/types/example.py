class Example:
    def __init__(
        self,
        identifier,
        question,
        answer,
        qa_data=None,
        alternative_questions=None,
        variations_created_at="",
        metrics=None,
    ):
        if alternative_questions is None:
            self.alternative_questions = {}
        else:
            self.alternative_questions = alternative_questions
        if qa_data is None:
            self.qa_data = {}
        else:
            self.qa_data = qa_data
        if metrics is None:
            self.metrics = {}
        else:
            self.metrics = metrics
        self.identifier = identifier
        self.question = question
        self.answer = answer
        self.variations_created_at = variations_created_at
        self.metrics = {}

    def __json__(self):
        return {
            "identifier": self.identifier,
            "question": self.question,
            "answer": self.answer,
            "alternative_questions": self.alternative_questions,
            "qa_data": self.qa_data,
            "variations_created_at": self.variations_created_at,
            "metrics": self.metrics,
        }
