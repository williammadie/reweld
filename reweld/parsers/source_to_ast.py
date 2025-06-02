import ast


class SourceToAST:
    """
    Converts Python source code into an abstract syntax tree (AST).
    """


    @staticmethod
    def parse(source_code: str) -> ast.AST:
        """
        Parse Python source code into an AST.

        Args:
            source_code (str): The Python source code to parse.

        Returns:
            ast.AST: The root of the parsed AST.

        Raises:
            SyntaxError: If the source code contains syntax errors.
        """
        try:
            return ast.parse(source_code)
        except SyntaxError as e:
            raise SyntaxError(f"Syntax error while parsing source: {e}") from e
