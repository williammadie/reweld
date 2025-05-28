from reweld.models.uml.uml_attribute import UmlAttribute
from reweld.models.uml.uml_method import UmlMethod


class UmlClass:
    def __init__(self, name: str, attributes: list, methods: list, extends: str = "object", parent_attributes: list = []):
        self.name = name
        self.extends = extends
        self.attributes = [UmlAttribute(name=attr["name"], type_=attr["type"]) for attr in attributes]
        self.methods = [UmlMethod(m["name"], m.get("returnType", "None"), m.get("parameters", [])) for m in methods]
        self.parent_attributes = [UmlAttribute(name=attr["name"], type_=attr["type"]) for attr in parent_attributes or []]

    def to_source(self) -> str:
        if self.extends == "object" or not self.extends:
            lines = [f"class {self.name}:"]
        else:
            lines = [f"class {self.name}({self.extends}):"]

        if not self.attributes and not self.methods:
            lines.append("    pass")
            return "\n".join(lines)

        # Constructor parameters: combine parent and own attributes
        all_attrs = self.parent_attributes + self.attributes
        all_params = ", ".join([attr.to_init_param() for attr in all_attrs])
        lines.append(f"    def __init__(self, {all_params}):")

        # super().__init__(...) with parent attr names
        if self.parent_attributes:
            args = ", ".join(attr.name for attr in self.parent_attributes)
            lines.append(f"        super().__init__({args})")

        # Child attribute assignments
        for attr in self.attributes:
            lines.append(attr.to_init_assignment())

        for method in self.methods:
            lines.append("")
            lines.append(method.to_source())

        return "\n".join(lines)