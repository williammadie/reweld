import ast


class ASTToSource:
    """
    Converts an abstract syntax tree (AST) back into Python source code.
    """

    @staticmethod
    def convert(tree: ast.AST) -> str:
        """
        Generate Python source code from an AST.

        Args:
            tree (ast.AST): The AST to unparse.

        Returns:
            str: Python source code.

        Raises:
            TypeError: If the input is not an AST.
            ValueError: If unparsing fails.
        """
        if not isinstance(tree, ast.AST):
            raise TypeError("Input must be an instance of ast.AST")

        try:
            return ast.unparse(tree)
        except Exception as e:
            raise ValueError(f"Failed to generate source from AST: {e}") from e
