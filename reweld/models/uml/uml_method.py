from aidd.models.uml.type_mapper import TypeMapper


class UmlMethod:
    def __init__(self, name: str, return_type: str, parameters: list):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters  # list of UmlAttribute or tuples

    def to_source(self):
        params_str = ", ".join([
            f"{p['name']}: {TypeMapper.map(p['type'])}" 
            for p in self.parameters
        ])
        return_type = TypeMapper.map(self.return_type)
        return f"    def {self.name}(self{', ' + params_str if params_str else ''}) -> {return_type}:\n        pass"
