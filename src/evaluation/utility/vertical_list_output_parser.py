from typing import List
from langchain.schema import BaseOutputParser


class VerticalListOutputParser(BaseOutputParser[List[str]]):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str) -> List[str]:
        """Parse the output of an LLM call."""
        split_answers = text.strip().split("\n")
        try:
            output = [string.split(". ", 1)[1] for string in split_answers]
        except IndexError as e:
            print(split_answers)
            output = split_answers
        filter(None, output)
        return output
