"""
An Enum is used to give meaning to values: 42 is THE answer, 666 the devil's number, [...]
If mixed with another type (str, int, ...) it inherits its functionality and
    upon using that type's functionality the value of the Enum-Name is used
"""

from enum import Enum

class Fibonacci_INT(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 5
    SIX = 8
print(Fibonacci_INT.FOUR, Fibonacci_INT.FOUR + Fibonacci_INT.FOUR)


class Fibonacci_STR(str, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 5
    SIX = 8
print(Fibonacci_STR.FOUR, Fibonacci_STR.FOUR + Fibonacci_STR.FOUR)


def return_fib_int():
    return f"this is {Fibonacci_INT.FOUR}"

def return_fib_str():
    return f"this is {Fibonacci_STR.FOUR}"

def return_fib_upper():
    return Fibonacci_STR.FOUR.upper()


print(return_fib_int())
print(return_fib_str())
print(return_fib_upper())


print(type(Fibonacci_INT), type(Fibonacci_INT.FOUR))
print(Fibonacci_INT.FOUR == 5)


# TESTING INT-ENUM
class HTTPCodes(int, Enum):
    Ok = 200
    Accepted = 202
    NotFound = 404
    InternalServerError = 500
    BadGateway = 502

class Website:
    def __init__(self, title: str, HTTPstatus: int, users: int):
        self.title = title
        self.HTTPstatus = HTTPstatus
        self.users = users

stackoverflow = Website(title='Stack Overflow', HTTPstatus=202, users=1_000_000)

if stackoverflow.HTTPstatus == HTTPCodes.BadGateway:
    print('we are working on it... !')
elif stackoverflow.HTTPstatus == HTTPCodes.Accepted:
    print('Request accepted')
elif HTTPCodes.Ok == stackoverflow.HTTPstatus :
    print('Connection successful!')
else:
    print(stackoverflow.HTTPstatus)


# TESTING STR-ENUM
class StudyDepartments(str, Enum):
    SE = 'Software Engineering'
    ID = 'Interaction Design'
    PM = 'Product Management'

class Student:
    def __init__(self, name, major, age, sexy):
        self.name = name
        self.major = major
        self.age = age
        self.sexy = sexy

hanno = Student(name='Hanno', major='Software Engineering', age=23, sexy='very true')

if hanno.major == StudyDepartments.PM:
    print(f'Why are you studying {StudyDepartments.PM} FFS')
elif hanno.major == StudyDepartments.ID:
    print(f"I mean... {StudyDepartments.ID} is not too bad, I guess?")
elif hanno.major == StudyDepartments.SE:
    print(f"Oh boy, now we're talking! {StudyDepartments.SE} is the way to go!")


class Animal(str, Enum):
    dog = 1
    cat = 2

if type(Animal.dog) is type(Animal.cat):
    print('Dog and Cat have the same type: Animal')