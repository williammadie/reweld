# utils/type_mapper.py

class TypeMapper:
    _type_mapping = {
        "String": "str",
        "int": "int",
        "float": "float",
        "double": "float",
        "boolean": "bool",
        "void": "None"
    }

    @classmethod
    def map(cls, uml_type: str) -> str:
        return cls._type_mapping.get(uml_type, uml_type)
