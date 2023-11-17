from abc import ABC, abstractmethod


class LLMClient(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def send_data_to_api(self, data):
        pass
