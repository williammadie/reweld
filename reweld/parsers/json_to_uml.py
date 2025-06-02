from reweld.models.uml_model import UMLClass, Method, Attribute


class JSONToUML:
    """
    Converts a JSON structure representing a UML class diagram into UMLClass objects.
    """

    @staticmethod
    def convert(uml_json: list[dict]) -> list[UMLClass]:
        """
        Convert a list of UML class dictionaries (from JSON) into UMLClass objects.

        Args:
            uml_json (list[dict]): The JSON-parsed list representing UML classes.

        Returns:
            list[UMLClass]: A list of UMLClass objects.
        """
        uml_classes = []

        for cls in uml_json:
            name = cls.get("name")
            bases = cls.get("bases", [])

            attributes = [
                Attribute(name=attr["name"]) if isinstance(attr, dict) else Attribute(name=attr)
                for attr in cls.get("attributes", [])
            ]

            methods = [
                Method(
                    name=method["name"],
                    args=method.get("args", [])
                )
                for method in cls.get("methods", [])
            ]

            uml_classes.append(UMLClass(
                name=name,
                bases=bases,
                attributes=attributes,
                methods=methods
            ))

        return uml_classes
