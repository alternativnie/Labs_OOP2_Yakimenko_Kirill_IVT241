from abc import ABC, abstractmethod


class DeliveryStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, weight: float, distance: float) -> float:
        pass

    @abstractmethod
    def get_delivery_time(self) -> str:
        pass

    @abstractmethod
    def get_max_weight(self) -> float:
        pass

    @abstractmethod
    def get_time_score(self) -> int:

        pass


class CourierDelivery(DeliveryStrategy):
    def calculate_cost(self, weight: float, distance: float) -> float:
        return 200 + weight * 30 + distance * 20

    def get_delivery_time(self) -> str:
        return "1-2 дня"

    def get_max_weight(self) -> float:
        return 100.0

    def get_time_score(self) -> int:
        return 2


class PostDelivery(DeliveryStrategy):
    def calculate_cost(self, weight: float, distance: float) -> float:
        return 100 + weight * 15 + distance * 5

    def get_delivery_time(self) -> str:
        return "3-7 дней"

    def get_max_weight(self) -> float:
        return 30.0

    def get_time_score(self) -> int:
        return 3


class DroneDelivery(DeliveryStrategy):
    def calculate_cost(self, weight: float, distance: float) -> float:
        if weight > 5:
            return float('inf')
        return 500 + weight * 50 + distance * 10

    def get_delivery_time(self) -> str:
        return "30 минут - 2 часа"

    def get_max_weight(self) -> float:
        return 5.0

    def get_time_score(self) -> int:
        return 1


class Order:
    def __init__(self, item_name: str, weight: float, distance: float, priority: str = "price"):
        self.item_name = item_name
        self.weight = weight
        self.distance = distance
        self.priority = priority
        self._delivery_strategy = self._choose_best_strategy()

    def _choose_best_strategy(self) -> DeliveryStrategy:
        strategies = [CourierDelivery(), PostDelivery(), DroneDelivery()]

        possible = []
        for strategy in strategies:
            if self.weight <= strategy.get_max_weight():
                cost = strategy.calculate_cost(self.weight, self.distance)
                if cost != float('inf'):
                    possible.append(strategy)

        if not possible:
            return CourierDelivery()

        if self.priority == "price":
            best = min(possible, key=lambda s: s.calculate_cost(self.weight, self.distance))
        else:
            best = min(possible, key=lambda s: s.get_time_score())

        return best

    def calculate_delivery(self) -> dict:
        return {
            "item": self.item_name,
            "cost": self._delivery_strategy.calculate_cost(self.weight, self.distance),
            "delivery_time": self._delivery_strategy.get_delivery_time(),
            "strategy": self._delivery_strategy.__class__.__name__
        }


if __name__ == "__main__":
    print("Книга (0.5кг, 5км) | БЫСТРО ")
    order1 = Order("Книга", weight=0.5, distance=5, priority="speed")
    result1 = order1.calculate_delivery()
    print(f"{result1['strategy']} | {result1['cost']} руб. | {result1['delivery_time']}\n")

    print("Телевизор (8кг, 15км) | БЫСТРО")
    order2 = Order("Телевизор", weight=8, distance=15, priority="speed")
    result2 = order2.calculate_delivery()
    print(f"{result2['strategy']} | {result2['cost']} руб. | {result2['delivery_time']}\n")

    print("Холодильник (40кг, 30км) | ДЁШЕВО")
    order3 = Order("Холодильник", weight=40, distance=30, priority="price")
    result3 = order3.calculate_delivery()
    print(f"{result3['strategy']} | {result3['cost']} руб. | {result3['delivery_time']}\n")

    print("Ноутбук (2кг, 10км) | ДЁШЕВО")
    order4 = Order("Ноутбук", weight=2, distance=10, priority="price")
    result4 = order4.calculate_delivery()
    print(f"{result4['strategy']} | {result4['cost']} руб. | {result4['delivery_time']}\n")
