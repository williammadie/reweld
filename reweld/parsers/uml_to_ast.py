import ast
from reweld.models.uml_model import UMLClass, Method, Attribute


class UMLToAST:
    """
    Converts UMLClass objects to Python AST (abstract syntax tree).
    """

    @staticmethod
    def convert(uml_classes: list[UMLClass]) -> ast.Module:
        """
        Convert a list of UMLClass objects into an ast.Module representing the code.

        Args:
            uml_classes (list[UMLClass]): UML class diagram.

        Returns:
            ast.Module: The top-level module node.
        """
        class_nodes = [UMLToAST._class_to_ast(cls) for cls in uml_classes]
        return ast.Module(body=class_nodes, type_ignores=[])

    @staticmethod
    def _class_to_ast(cls: UMLClass) -> ast.ClassDef:
        """
        Convert a single UMLClass to an ast.ClassDef node.

        Args:
            cls (UMLClass): The UML class.

        Returns:
            ast.ClassDef: The class definition in AST.
        """
        bases = [ast.Name(id=base, ctx=ast.Load()) for base in cls.bases]

        # Attributes assigned in __init__
        init_body = []
        for attr in cls.attributes:
            assign = ast.Assign(
                targets=[
                    ast.Attribute(
                        value=ast.Name(id='self', ctx=ast.Load()),
                        attr=attr.name,
                        ctx=ast.Store()
                    )
                ],
                value=ast.Constant(value=None)  # default: None
            )
            init_body.append(assign)

        # Construct __init__ if needed
        init_method = None
        for method in cls.methods:
            if method.name == "__init__":
                args = [ast.arg(arg=arg) for arg in method.args]
                init_args = ast.arguments(
                    posonlyargs=[],
                    args=args,
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]
                )
                init_method = ast.FunctionDef(
                    name="__init__",
                    args=init_args,
                    body=init_body or [ast.Pass()],
                    decorator_list=[]
                )

        method_nodes = []
        for method in cls.methods:
            if method.name == "__init__" and init_method:
                method_nodes.append(init_method)
                continue

            args = [ast.arg(arg=arg) for arg in method.args]
            method_args = ast.arguments(
                posonlyargs=[],
                args=args,
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
            )

            method_node = ast.FunctionDef(
                name=method.name,
                args=method_args,
                body=[ast.Pass()],
                decorator_list=[]
            )
            method_nodes.append(method_node)

        return ast.ClassDef(
            name=cls.name,
            bases=bases,
            keywords=[],
            body=method_nodes,
            decorator_list=[]
        )
