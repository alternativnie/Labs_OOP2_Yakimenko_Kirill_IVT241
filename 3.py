from abc import ABC, abstractmethod
import random


class Notification(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> dict:
        pass


class EmailNotification(Notification):
    def send(self, recipient: str, message: str) -> dict:
        return {"type": "email", "status": "sent", "details": f"Email на {recipient}"}


class SMSNotification(Notification):
    def send(self, recipient: str, message: str) -> dict:
        return {"type": "sms", "status": "sent", "details": f"SMS на {recipient}"}


class PushNotification(Notification):
    def send(self, recipient: str, message: str) -> dict:
        return {"type": "push", "status": "sent", "details": f"Push на {recipient}"}


class TelegramNotification(Notification):
    def send(self, recipient: str, message: str) -> dict:
        return {"type": "telegram", "status": "sent", "details": f"Telegram на {recipient}"}


class NotificationFactory(ABC):
    @abstractmethod
    def create_notification(self) -> Notification:
        pass


class EmailFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return EmailNotification()


class SMSFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return SMSNotification()


class PushFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return PushNotification()


class TelegramFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return TelegramNotification()


def send_notification(factory: NotificationFactory, recipient: str, message: str) -> dict:
    notification = factory.create_notification()
    return notification.send(recipient, message)



if __name__ == "__main__":
    message = "Ваш заказ подтвержден!"

    print("=== ВЫБОР ФАБРИКИ ===\n")

    user_settings = {"notification_method": "telegram"}
    factory = TelegramFactory() if user_settings["notification_method"] == "telegram" else EmailFactory()
    recipient = "@john_doe"
    result = send_notification(factory, recipient, message)
    print(f"1. Настройки пользователя: {result['type']}, {message}")

    is_urgent = True
    factory = SMSFactory() if is_urgent else EmailFactory()
    result = send_notification(factory, "+7-999-123-45-67", "Код: 123456")
    print(f"2. Срочное сообщение: {result['type']}, {message}")

    factory = random.choice([EmailFactory(), SMSFactory(), PushFactory(), TelegramFactory()])
    result = send_notification(factory, "user", "Тест")
    print(f"3. Случайный выбор: {result['type']}, {message}")

    current_hour = 15
    factory = EmailFactory() if 9 <= current_hour <= 21 else SMSFactory()
    result = send_notification(factory, "user@mail.com", "Уведомление")
    print(f"4. Время ({current_hour}:00): {result['type']}, {message}")