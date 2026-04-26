from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass # frozen=True делает объект неизменяемым (как кортеж)
class BaseEntity:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class User(BaseEntity):
    name: str = ""
    email: str = ""
    age: int = 0

if __name__ == "__main__":
    user = User(name="Алексей", email="alex@mail.com", age=25)

    print(f"Пользователь: {user.name}")
    print(f"ID (создан базой): {user.id}")
    print(f"Дата создания: {user.created_at}")
    print(f"Весь объект: {user}")
