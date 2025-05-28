import os
from reweld.models.uml.uml_model import UmlModel
from reweld.path_handler import PathHandler

def main():
    uml_model = UmlModel(
        os.path.join(PathHandler.test_directory_path(), "data", "uml_model_2.json")
    )
    print(uml_model.to_source_code())


if __name__ == "__main__":
    main()
