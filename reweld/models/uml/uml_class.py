from reweld.models.uml.uml_attribute import UmlAttribute
from reweld.models.uml.uml_method import UmlMethod


class UmlClass:
    def __init__(self, name: str, attributes: list, methods: list, extends: str = "object"):
        self.name = name
        self.attributes = [UmlAttribute(name=attr["name"], type_=attr["type"]) for attr in attributes]
        self.methods = [UmlMethod(m["name"], m.get("returnType", "None"), m.get("parameters", [])) for m in methods]
        self.extends = extends

    def to_source(self) -> str:
        # Class signature
        if self.extends == "object" or not self.extends:
            lines = [f"class {self.name}:"]
        else:
            lines = [f"class {self.name}({self.extends}):"]

        if not self.attributes and not self.methods:
            lines.append("    pass")
            return "\n".join(lines)

        # Constructor
        if self.attributes:
            params = ", ".join([attr.to_init_param() for attr in self.attributes])
            lines.append(f"    def __init__(self, {params}):")
            lines.extend([attr.to_init_assignment() for attr in self.attributes])
        else:
            lines.append("    def __init__(self):")
            lines.append("        pass")

        for method in self.methods:
            lines.append("")
            lines.append(method.to_source())

        return "\n".join(lines)