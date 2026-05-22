class Employee:
    __company_name = "Mark Inc"

    def mark_attendance(self):
        print("Marked attendance for {}".format(self.__company_name))


class Programmer(Employee):
    def __init__(self, bonus_percentage):
        self.bonus_percentage = bonus_percentage

    def calculate_bonuses(self):
        print("Bonus calculation done - Bonus : {}, Company name : ".format(self.bonus_percentage))


if __name__ == '__main__':
    john_programmer = Programmer(10)
 
    # __variable is the convient uses as Private Modifier

    john_programmer.calculate_bonuses()
    john_programmer.mark_attendance()