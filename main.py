from aidd.models.uml.uml_model import UmlModel

def main():
    uml_model = UmlModel(
        "/home/william/Projets/aidd/test/uml_model/data/model_1.json"
    )
    print(uml_model.to_source_code())


if __name__ == "__main__":
    main()
