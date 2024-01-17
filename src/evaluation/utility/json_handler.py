import json
import os

import constants
from evaluation.types.example import Example


class JsonHandler:
    def __init__(self):
        self.folder_path_variations = constants.QAP_VARIATIONS_OUTPUT_FOLDER

    def load_generated_variations(self):
        # Iterate over all files in the folder
        examples = []
        for filename in os.listdir(self.folder_path_variations):
            file_path = os.path.join(self.folder_path_variations, filename)

            # Check if the file is a regular file (not a directory)
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    try:
                        # Load the JSON data from the file
                        raw = json.load(file)
                        example = Example(**raw)
                        # Now you can work with the deserialized JSON object
                        # For example, print the content
                        print(f"Contents of {filename}: {raw}")

                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in {filename}: {e}")
                    examples.append(example)
        return examples
