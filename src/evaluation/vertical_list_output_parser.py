from typing import List
from langchain.schema import BaseOutputParser


class VerticalListOutputParser(BaseOutputParser[List[str]]):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str) -> List[str]:
        """Parse the output of an LLM call."""
        split_answers = text.strip().split("\n")
        output = [string.split(". ", 1)[1] for string in split_answers]
        return output
