
from aidd.models.uml.type_mapper import TypeMapper


class UmlAttribute:
    def __init__(self, name: str, type_: str):
        self.name = name
        self.type_ = type_

    def to_init_param(self):
        return f"{self.name}: {self.map_type()}"

    def to_init_assignment(self):
        return f"        self.{self.name} = {self.name}"

    def map_type(self):
        return TypeMapper.map(self.type_)