class Employee:
    company_name = "Mark Inc"

    def mark_attendance(self):
        print("Marked attendance for {}".format(self.company_name))


class Programmer(Employee):
    def __init__(self, bonus_percentage):
        self.bonus_percentage = bonus_percentage

    def calculate_bonuses(self):
        print("Bonus calculation done - Bonus : {}, Company name : {}".format(self.bonus_percentage, self.company_name))

    def mark_attendance(self):
        print("Mark attendance for Programmer")
        # Parent class is to be overrided.
        super().mark_attendance()


if __name__ == '__main__':
    john_programmer = Programmer(10)
    john_programmer.calculate_bonuses()
    john_programmer.mark_attendance()