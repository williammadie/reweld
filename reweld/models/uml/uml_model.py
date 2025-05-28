import json
from typing import Self

from aidd.models.uml.uml_class import UmlClass

class UmlModel:

    def __init__(self: Self, file_path: str):
        self.file_path = file_path
        self.model = self.load_from_json()
        self.classes = self.parse_classes()
    
    def load_from_json(self: Self) -> dict:
        with open(self.file_path, encoding="utf8") as f:
            file_content = f.read()
        return json.loads(file_content)
    
    def parse_classes(self):
        return [
            UmlClass(
                cls["name"],
                cls.get("attributes", []),
                cls.get("methods", []),
                cls.get("extends", "object")
            )
            for cls in self.model.get("classes", [])
        ]

    def to_source_code(self: Self) -> str:
        return "\n\n".join(cls.to_source() for cls in self.classes)
    
    @staticmethod
    def map_type_static(uml_type: str) -> str:
        type_mapping = {
            "String": "str",
            "int": "int",
            "float": "float",
            "double": "float",
            "boolean": "bool",
            "void": "None"
        }
        return type_mapping.get(uml_type, uml_type)
