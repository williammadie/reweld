import json
from pathlib import Path
from ast import AST

from reweld.parsers.ast_to_uml import ASTToUML
from reweld.models.uml_model import UMLClass
from reweld.parsers.uml_to_json import UMLToJSON
from reweld.parsers.json_to_uml import JSONToUML


class ClassDiagram:
    def __init__(
            self,
            ast_tree: AST | None = None,
            uml_classes: list[UMLClass] | None = None
            ):
        self.ast_tree = ast_tree
        self.uml_classes = uml_classes or []

    @classmethod
    def from_ast(cls, ast_tree: AST):
        """
        Create a ClassDiagram instance from an AST.
        """
        uml_classes = ASTToUML.convert(ast_tree)
        return cls(ast_tree=ast_tree, uml_classes=uml_classes)

    @classmethod
    def from_file(cls, filepath: str):
        """
        Create a ClassDiagram instance from a JSON file containing UML class definitions.
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"No such file: '{filepath}'")

        with path.open("r", encoding="utf-8") as f:
            uml_json = json.load(f)

        uml_classes = JSONToUML.convert(uml_json)
        return cls(ast_tree=None, uml_classes=uml_classes)

    def to_json(self) -> str:
        """
        Serialize the UML class diagram to a JSON string.
        """
        return UMLToJSON().convert(self.uml_classes)

    def save_to_file(self, filepath: str):
        """
        Save the UML class diagram to a JSON file.
        """
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(json.loads(self.to_json()), f, indent=4)

    def __repr__(self):
        return f"<ClassDiagram with {len(self.uml_classes)} class(es)>"
