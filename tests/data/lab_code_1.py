class MyClass:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.value = new_value

    def increment_value(self, increment=1):
        self.value += increment
        return self.value

    def reset_value(self):
        self.value = 0
        return self.value