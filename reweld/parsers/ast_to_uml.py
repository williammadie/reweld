import ast
from reweld.models.uml_model import UMLClass, Method, Attribute


class ASTToUML:
    @staticmethod
    def convert(tree: ast.AST) -> list[UMLClass]:
        """
        Convert a Python AST tree into a list of UMLClass representations.

        Args:
            tree (ast.AST): The abstract syntax tree of the Python source code.

        Returns:
            List[UMLClass]: A list of UMLClass objects representing the class diagram.
        """
        converter = ASTToUML._ASTToUMLConverter(tree)
        converter.visit(tree)
        return converter.to_uml_classes()

    class _ASTToUMLConverter(ast.NodeVisitor):
        def __init__(self, tree: ast.AST):
            self.tree = tree
            self.class_diagram = []

        def visit_ClassDef(self, node):
            class_info = {
                "name": node.name,
                "bases": [base.id for base in node.bases if isinstance(base, ast.Name)],
                "methods": [],
                "attributes": []
            }

            for body_item in node.body:
                if isinstance(body_item, ast.FunctionDef):
                    method_info = {
                        "name": body_item.name,
                        "args": [arg.arg for arg in body_item.args.args]
                    }
                    class_info["methods"].append(method_info)

                    if body_item.name == "__init__":
                        for stmt in ast.walk(body_item):
                            if isinstance(stmt, ast.Assign):
                                for target in stmt.targets:
                                    if (
                                        isinstance(target, ast.Attribute)
                                        and isinstance(target.value, ast.Name)
                                        and target.value.id == "self"
                                    ):
                                        class_info["attributes"].append(target.attr)

            self.class_diagram.append(class_info)
            self.generic_visit(node)

        def to_uml_classes(self) -> list[UMLClass]:
            uml_classes = []
            for cls in self.class_diagram:
                uml_class = UMLClass(
                    name=cls["name"],
                    bases=cls["bases"],
                    attributes=[Attribute(name=a) for a in cls["attributes"]],
                    methods=[
                        Method(name=m["name"], args=m["args"]) for m in cls["methods"]
                    ],
                )
                uml_classes.append(uml_class)
            return uml_classes
