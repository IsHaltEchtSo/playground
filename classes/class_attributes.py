"""
The class attribute can be accessed from the class and the object!
A property is a function that is accessed like an attribute
"""

class Dog:
    dog_count = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Dog.dog_count += 1
        self.names = []

    def __del__(self):
        print(f"Goodbye {self.name}")
        Dog.dog_count -= 1

    @property
    def current_name(self):
        return self.name

    @current_name.setter
    def current_name(self, value):
        if value == self.name:
            raise ValueError("The new name must be different from the old name")
        elif value in self.names:
            raise ValueError(f"The new name needs to be different from the old names {self.names}")
        else:
            self.names.append(self.name)
            self.name = value
    

print(Dog.dog_count)  # 0

russel = Dog(name='Russel', age=2)
print(Dog.dog_count)  # 1
print(russel.dog_count)  # 1

pokko = Dog(name='Pokko', age=4)
print(Dog.dog_count)  # 2
print(pokko.dog_count)  # 2
print(russel.dog_count)  # 2

del russel
print(Dog.dog_count)  # 1
print(pokko.dog_count)  # 1

print(pokko.name)  # Pokko
pokko.current_name = 'pikko'
pokko.current_name = 'Pikko'
print(pokko.current_name, pokko.names)  # Pikko ['Pokko', 'pikko']
