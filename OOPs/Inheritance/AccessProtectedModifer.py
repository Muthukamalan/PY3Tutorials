class Employee:
    _company_name = "Mark Inc"

    def mark_attendance(self):
        print("Marked attendance for {}".format(self._company_name))


class Programmer(Employee):
    def __init__(self, bonus_percentage):
        self.bonus_percentage = bonus_percentage

    def calculate_bonuses(self):
        print("Bonus calculation done - Bonus : {}, Company name : {}".format(self.bonus_percentage, self._company_name))


if __name__ == '__main__':
    john_programmer = Programmer(10)   # Child class can use the _variable from parent class
    john_programmer.calculate_bonuses()
    john_programmer.mark_attendance()