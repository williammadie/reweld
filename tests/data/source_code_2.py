class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> None:
        pass

class Student(Person):
    def __init__(self, name: str, age: int, studentId: str):
        super().__init__(name, age)
        self.studentId = studentId

    def study(self) -> None:
        pass