class Employee:
    company_name = "Mark Inc"

    def mark_attendance(self):
        print("Marked attendance for {}".format(self.company_name))


class Administrator:
    admin_name = "Test admin"

    def print_admin(self):
        print(self.admin_name)


class Programmer(Employee, Administrator):
    def __init__(self, bonus_percentage):
        self.bonus_percentage = bonus_percentage

    def calculate_bonuses(self):
        print("Bonus calculation done - Bonus : {}, Company name : {}".format(self.bonus_percentage, self.company_name))
        print(self.admin_name)


if __name__ == '__main__':

    print(f"{Programmer.mro()}")

    john_programmer = Programmer(10)
    john_programmer.calculate_bonuses()
    john_programmer.mark_attendance()
    john_programmer.print_admin()