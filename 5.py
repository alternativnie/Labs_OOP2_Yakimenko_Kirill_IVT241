from abc import ABC, abstractmethod


class Beverage(ABC):

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass


class Espresso(Beverage):
    def get_description(self) -> str:
        return "Эспрессо"

    def get_cost(self) -> float:
        return 150.0


class Americano(Beverage):
    def get_description(self) -> str:
        return "Американо"

    def get_cost(self) -> float:
        return 180.0


class Latte(Beverage):
    def get_description(self) -> str:
        return "Латте"

    def get_cost(self) -> float:
        return 220.0


class BeverageDecorator(Beverage):
    def __init__(self, beverage: Beverage):
        self._beverage = beverage

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass


class MilkDecorator(BeverageDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + " + молоко"

    def get_cost(self) -> float:
        return self._beverage.get_cost() + 30.0


class SugarDecorator(BeverageDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + " + сахар"

    def get_cost(self) -> float:
        return self._beverage.get_cost() + 10.0


class WhippedCreamDecorator(BeverageDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + " + взбитые сливки"

    def get_cost(self) -> float:
        return self._beverage.get_cost() + 45.0


class CinnamonDecorator(BeverageDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + " + корица"

    def get_cost(self) -> float:
        return self._beverage.get_cost() + 20.0


class ChocolateDecorator(BeverageDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + " + шоколад"

    def get_cost(self) -> float:
        return self._beverage.get_cost() + 50.0


import random


if __name__ == "__main__":
    print("=== Добро пожаловать в Smart Coffee 2026! ===\n")

    bases = [Espresso, Americano, Latte]

    available_decorators = [
        MilkDecorator,
        SugarDecorator,
        WhippedCreamDecorator,
        CinnamonDecorator,
        ChocolateDecorator
    ]

    for i in range(1, 4):
        base_class = random.choice(bases)
        beverage = base_class()

        num_additions = random.randint(1, 5)

        for _ in range(num_additions):
            decorator_class = random.choice(available_decorators)
            beverage = decorator_class(beverage)

        print(f"Заказ №{i}: {beverage.get_description()}")
        print(f"Итоговая цена: {beverage.get_cost()} руб.")
        print("-" * 30)