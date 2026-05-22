from abc import ABCMeta, abstractmethod


class Car(metaclass=ABCMeta):
    @abstractmethod
    def apply_breaks(self) -> None:
        pass


class ElectricCar(Car):
    def apply_breaks(self):
        print("Apply breaks in Electric Car")


class PetrolCar(Car):
    def apply_breaks(self) -> None:
        print("Apply break in Petrol Cars")


if __name__ == "__main__":
    tesla = ElectricCar()
    tesla.apply_breaks()

    audi = PetrolCar()
    audi.apply_breaks()
