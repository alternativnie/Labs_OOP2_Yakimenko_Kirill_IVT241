from abc import ABC, abstractmethod


class OrderState(ABC):

    @abstractmethod
    def pay(self, order):
        pass

    @abstractmethod
    def ship(self, order):
        pass

    @abstractmethod
    def deliver(self, order):
        pass

    @abstractmethod
    def cancel(self, order):
        pass


class NewOrderState(OrderState):

    def pay(self, order):
        print("Оплата принята. Заказ переходит в состояние 'Оплачен'")
        order.state = PaidOrderState()

    def ship(self, order):
        print("Нельзя отгрузить неоплаченный заказ")

    def deliver(self, order):
        print("Нельзя доставить неотгруженный заказ")

    def cancel(self, order):
        print("Заказ отменен")
        order.state = CancelledOrderState()


class PaidOrderState(OrderState):

    def pay(self, order):
        print("Заказ уже оплачен")

    def ship(self, order):
        print("Заказ передан в доставку")
        order.state = ShippedOrderState()

    def deliver(self, order):
        print("Сначала нужно отгрузить заказ")

    def cancel(self, order):
        print("Возврат средств. Заказ отменен")
        order.state = CancelledOrderState()


class ShippedOrderState(OrderState):

    def pay(self, order):
        print("Заказ уже оплачен и отгружен")

    def ship(self, order):
        print("Заказ уже отгружен")

    def deliver(self, order):
        print("Заказ доставлен покупателю")
        order.state = DeliveredOrderState()

    def cancel(self, order):
        print("Нельзя отменить отгруженный заказ")


class DeliveredOrderState(OrderState):

    def pay(self, order):
        print("Заказ уже оплачен и доставлен")

    def ship(self, order):
        print("Заказ уже доставлен")

    def deliver(self, order):
        print("Заказ уже доставлен")

    def cancel(self, order):
        print("Нельзя отменить доставленный заказ")


class CancelledOrderState(OrderState):

    def pay(self, order):
        print("Нельзя оплатить отмененный заказ")

    def ship(self, order):
        print("Нельзя отгрузить отмененный заказ")

    def deliver(self, order):
        print("Нельзя доставить отмененный заказ")

    def cancel(self, order):
        print("Заказ уже отменен")


class Order:

    def __init__(self, order_id: str):
        self.order_id = order_id
        self.state = NewOrderState()

    def pay(self):
        print(f"\n--- Заказ {self.order_id}: ПЛАТЕЖ ---")
        self.state.pay(self)

    def ship(self):
        print(f"--- Заказ {self.order_id}: ОТГРУЗКА ---")
        self.state.ship(self)

    def deliver(self):
        print(f"--- Заказ {self.order_id}: ДОСТАВКА ---")
        self.state.deliver(self)

    def cancel(self):
        print(f"--- Заказ {self.order_id}: ОТМЕНА ---")
        self.state.cancel(self)

    def get_status(self):
        return self.state.__class__.__name__.replace('OrderState', '')



if __name__ == "__main__":
    order = Order("A-123")

    print(f"Начальный статус: {order.get_status()}")

    order.pay()
    print(f"Статус после оплаты: {order.get_status()}")

    order.ship()
    print(f"Статус после отгрузки: {order.get_status()}")

    order.deliver()
    print(f"Статус после доставки: {order.get_status()}")

    order.cancel()

    print("\n" + "=" * 50)
    order2 = Order("B-456")
    order2.cancel()
    print(f"Статус после отмены: {order2.get_status()}")

    order2.pay()