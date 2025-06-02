import json
from reweld.models.uml_model import UMLClass


class UMLToJSON:
    """
    Converts UMLClass objects into JSON-serializable structures.
    """

    @staticmethod
    def convert(uml_classes: list[UMLClass]) -> str:
        """
        Convert UMLClass objects to a formatted JSON string.

        Args:
            uml_classes (list[UMLClass]): List of UMLClass instances.

        Returns:
            str: JSON string representation of UML classes.
        """
        return json.dumps(
            [UMLToJSON._class_to_dict(cls) for cls in uml_classes],
            indent=4
        )

    @staticmethod
    def _class_to_dict(uml_class: UMLClass) -> dict:
        """
        Convert a UMLClass instance into a dictionary.

        Args:
            uml_class (UMLClass): The UMLClass instance to convert.

        Returns:
            dict: Dictionary representation of the class.
        """
        return {
            "name": uml_class.name,
            "bases": uml_class.bases,
            "attributes": [{"name": attr.name} for attr in uml_class.attributes],
            "methods": [
                {"name": method.name, "args": method.args} for method in uml_class.methods
            ]
        }
