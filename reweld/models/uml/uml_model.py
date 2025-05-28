import json
from typing import Self

from reweld.models.uml.uml_class import UmlClass

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
        class_defs = {cls["name"]: cls for cls in self.model.get("classes", [])}

        def get_parent_attributes(class_def):
            parent_name = class_def.get("extends", "object")
            if parent_name == "object":
                return []
            parent_def = class_defs.get(parent_name)
            if not parent_def:
                return []
            return parent_def.get("attributes", [])
    
        return [
            UmlClass(
                cls["name"],
                cls.get("attributes", []),
                cls.get("methods", []),
                cls.get("extends", "object"),
                parent_attributes=get_parent_attributes(cls)
            )
            for cls in self.model.get("classes", [])
        ]

    def to_source_code(self: Self) -> str:
        return "\n\n".join(cls.to_source() for cls in self.classes)
