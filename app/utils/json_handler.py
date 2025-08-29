import os
import json


class JSONHandler:
    def read_json(self, file_path):
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, "r") as file:
            content = file.read().strip()
            if not content:
                return []
            
            return json.loads(content)

    def write_json(self, file_path, data):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)