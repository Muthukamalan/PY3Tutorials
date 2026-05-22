class Employee:
    def __init__(self, salary):
        self.salary = salary

    def __add__(self, other):
        return self.salary + other.salary


if __name__ == '__main__':
    emp1 = Employee(1000)
    emp2 = Employee(2000)


    # __add__ function Overloaded for Employee Object 
    print(emp1 + emp2)