import json
import os


class Persistence:
    def __init__(self, output_file=None):
        self.output_file = output_file

    def save(self, colleges_data):
        if not self.output_file:
            return
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(colleges_data, f, indent=2, ensure_ascii=False)
