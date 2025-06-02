import os
import ast
from reweld.models.class_diagram import ClassDiagram
from reweld.models.source_code_file import SourceCodeFile
from reweld.models.uml.uml_model import UmlModel
from reweld.path_handler import PathHandler
from reweld.sync.diagram_sync import DiagramSync

def uml_to_code():
    uml_model = UmlModel(
        os.path.join(PathHandler.test_directory_path(), "data", "uml_model_2.json")
    )
    print(uml_model.to_source_code())

def code_to_ast():
    ast_tree = SourceCodeFile.from_file(
        os.path.join(PathHandler.test_directory_path(), "data", "source_code_1.py")
    ).to_ast()
    print(ast.dump(ast_tree, indent=4))

    ClassDiagram.from_ast(ast_tree).save_to_file("test.json")

def diagram_sync():

    syncer = DiagramSync(
        source_path=os.path.join(PathHandler.test_directory_path(), "data", "lab_code_1.py"),
        diagram_path=os.path.join(PathHandler.test_directory_path(), "data", "lab_uml_1.json")
    )
    syncer.start()

if __name__ == "__main__":
    diagram_sync()
