from ast import AST

from reweld.parsers.source_to_ast import SourceToAST
from reweld.parsers.ast_to_source import ASTToSource


class SourceCodeFile:
    def __init__(self, source_code: str, ast_tree: AST):
        self.source_code = source_code
        self.ast_tree = ast_tree

    @classmethod
    def from_file(cls, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as file:
            source_code = file.read()
        ast_tree = SourceToAST.parse(source_code)
        return SourceCodeFile(source_code=source_code, ast_tree=ast_tree)

    @classmethod
    def from_ast(self, ast_tree):
        source_code = ASTToSource.generate(ast_tree)
        return SourceCodeFile(source_code=source_code, ast_tree=ast_tree)
    
    def to_ast(self):
        if self.ast_tree is None:
            self.ast_tree = SourceToAST.parse(self.source_code)
        return self.ast_tree

    def get_source_code(self):
        if self.source_code is None:
            raise ValueError("Source code is not set.")
        return self.source_code