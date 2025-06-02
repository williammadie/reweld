from dataclasses import dataclass, field
from typing import List


@dataclass
class Attribute:
    """Represents a class attribute."""
    name: str


@dataclass
class Method:
    """Represents a method in a class."""
    name: str
    args: List[str] = field(default_factory=list)


@dataclass
class UMLClass:
    """Represents a class in the UML diagram."""
    name: str
    bases: List[str] = field(default_factory=list)
    attributes: List[Attribute] = field(default_factory=list)
    methods: List[Method] = field(default_factory=list)
