class Car:

    def __init__(self, name):
        print("Constructor called")
        self.name = name

    def accelerate(self):
        color = "red"
        print("Accelerating car {} having color {}".format(self.name, color))


if __name__ == '__main__':
    car = Car("BMW")
    car.accelerate()

    car.name = "Maruthis"
    print(car.name)