import os
import difflib
import unittest

import autopep8


from reweld.models.uml.uml_model import UmlModel
from reweld.path_handler import PathHandler

class TestUmlModelToSourceCode(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(PathHandler.test_directory_path(), "data")
    
    def run_code_generation(self, uml_json_filename: str, source_code_filename: str) -> tuple:
        """
        Runs the code generation process for a given UML JSON file and source code file."""
        uml_json_path = os.path.join(self.data_dir, uml_json_filename)
        source_code_path = os.path.join(self.data_dir, source_code_filename)

        uml_model = UmlModel(uml_json_path)

        with open(source_code_path, 'r', encoding="utf8") as f:
            expected_code = f.read()

        return uml_model.to_source_code(), expected_code

    def assert_code_equal(self, generated_code: str, expected_code: str):
        """
        Compare two pieces of Python code after formatting them with autopep8.
        Ignores irrelevant formatting differences.
        """
        def format_code(code: str) -> str:
            return autopep8.fix_code(code, options={"aggressive": 1})

        formatted_generated = format_code(generated_code)
        formatted_expected = format_code(expected_code)

        if formatted_generated != formatted_expected:
            diff = difflib.unified_diff(
                formatted_expected.splitlines(),
                formatted_generated.splitlines(),
                fromfile='expected',
                tofile='generated',
                lineterm=''
            )
            diff_text = '\n' + '\n'.join(diff)
            self.fail(f"Formatted code does not match.\nDiff:\n{diff_text}")

    def test_generate_single_class(self):
        uml_json_path = os.path.join(self.data_dir, "uml_model_1.json")
        source_code_path = os.path.join(self.data_dir, "source_code_1.py")
        generated_code, expected_code = self.run_code_generation(uml_json_path, source_code_path)
        self.assert_code_equal(generated_code, expected_code)
    
    def test_generate_classes_with_inheritance(self):
        uml_json_path = os.path.join(self.data_dir, "uml_model_2.json")
        source_code_path = os.path.join(self.data_dir, "source_code_2.py")
        generated_code, expected_code = self.run_code_generation(uml_json_path, source_code_path)
        self.assert_code_equal(generated_code, expected_code)