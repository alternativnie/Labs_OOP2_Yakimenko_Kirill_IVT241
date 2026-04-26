from typing import Dict, List, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Message:

    event_type: str
    payload: Any
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)

    def __repr__(self):
        return f"Message({self.event_type}, id={self.message_id[:8]})"

class MessageBus:

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._async_handlers: Dict[str, List[Callable]] = {}
        self._message_history: List[Message] = []

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        print(f"[Bus] Подписка: {handler.__name__} -> {event_type}")

    def subscribe_async(self, event_type: str, handler: Callable):
        if event_type not in self._async_handlers:
            self._async_handlers[event_type] = []
        self._async_handlers[event_type].append(handler)

    def publish(self, message: Message) -> List[Any]:
        self._message_history.append(message)
        results = []

        if message.event_type in self._handlers:
            for handler in self._handlers[message.event_type]:
                try:
                    result = handler(message)
                    results.append(result)
                except Exception as e:
                    print(f"[Bus] Ошибка в обработчике {handler.__name__}: {e}")
                    results.append(None)

        if message.event_type in self._async_handlers:
            for handler in self._async_handlers[message.event_type]:
                self._run_async(handler, message)

        return results

    def _run_async(self, handler, message):
        import threading
        thread = threading.Thread(target=handler, args=(message,))
        thread.start()

    def get_history(self, event_type: str = None) -> List[Message]:
        if event_type:
            return [m for m in self._message_history if m.event_type == event_type]
        return self._message_history.copy()

    def clear(self):
        self._message_history.clear()


def on_user_registered(message: Message):
    print(f"[Handler] Приветственное письмо пользователю {message.payload['email']}")
    return "email_sent"

def on_user_registered_sms(message: Message):
    print(f"[Handler] SMS подтверждение на номер {message.payload['phone']}")
    return "sms_sent"

def on_order_created(message: Message):
    order = message.payload
    print(f"[Handler] Заказ #{order['id']} создан на сумму {order['total']} руб.")
    # Симуляция обработки
    return f"order_{order['id']}_processed"

def on_order_paid(message: Message):
    print(f"[Handler] Заказ {message.payload['order_id']} оплачен. Начинаем сборку...")
    return "assembly_started"

def on_payment_failed(message: Message):
    print(f"[ALERT] Ошибка оплаты заказа {message.payload['order_id']}: {message.payload['error']}")


def async_logging_handler(message: Message):
    import time
    time.sleep(0.5)
    print(f"[AsyncLogger] {message.timestamp}: {message.event_type} - {message.payload}")


if __name__ == "__main__":
    bus = MessageBus()

    bus.subscribe("user.registered", on_user_registered)
    bus.subscribe("user.registered", on_user_registered_sms)
    bus.subscribe("order.created", on_order_created)
    bus.subscribe("order.paid", on_order_paid)
    bus.subscribe("payment.failed", on_payment_failed)

    bus.subscribe_async("user.registered", async_logging_handler)
    bus.subscribe_async("order.created", async_logging_handler)

    print("=== Тестирование Шины Сообщений ===\n")

    print("--- Событие: Регистрация пользователя ---")
    user_data = {"username": "ivan_ivanov", "email": "ivan@example.com", "phone": "+79991234567"}
    msg_user = Message(event_type="user.registered", payload=user_data)
    bus.publish(msg_user)

    print("\n--- Событие: Создание заказа ---")
    order_data = {"id": 101, "total": 5500, "items": ["Книга", "Лампа"]}
    msg_order = Message(event_type="order.created", payload=order_data)
    bus.publish(msg_order)

    print("\n--- Событие: Оплата заказа ---")
    msg_paid = Message(event_type="order.paid", payload={"order_id": 101, "status": "success"})
    bus.publish(msg_paid)

    print("\n--- Событие: Ошибка платежа ---")
    msg_fail = Message(event_type="payment.failed", payload={"order_id": 102, "error": "Недостаточно средств"})
    bus.publish(msg_fail)

    import time

    time.sleep(1)

    print("\n=== Проверка истории сообщений ===")
    history = bus.get_history()
    print(f"Всего событий в шине: {len(history)}")
    for m in history:
        print(f"- [{m.timestamp.strftime('%H:%M:%S')}] {m.event_type} (ID: {m.message_id[:8]})")