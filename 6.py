import time
from dataclasses import dataclass
from typing import Callable, List, Dict


class Light:
    def __init__(self, room): self.room = room

    def switch(self, status): print(f"[{self.room}] Свет: {status}")


class Thermostat:
    def set_temp(self, t): print(f"[Термостат] Температура: {t}°C")


class MediaCenter:
    def play_movie(self, title): print(f"[Медиа] Запуск фильма: '{title}'")


@dataclass
class SmartCommand:
    action: Callable
    params: dict
    description: str

    def execute(self):
        return self.action(**self.params)


class MacroCommand:
    """Позволяет объединить несколько команд в одну"""

    def __init__(self, commands: List[SmartCommand], description: str):
        self.commands = commands
        self.description = description

    def execute(self):
        print(f"\n>>> Активация режима: {self.description}")
        for cmd in self.commands:
            print(f"  - {cmd.description}")
            cmd.execute()


class HomeCloud:
    def __init__(self):
        self.history = []
        self.scheduled_tasks = []

    def run(self, command):
        command.execute()
        self.history.append(command)

    def schedule(self, command, delay_seconds: int):
        print(f"[Таймер] Команда '{command.description}' выполнится через {delay_seconds} сек.")
        time.sleep(delay_seconds)
        self.run(command)


if __name__ == "__main__":

    hall_light = Light("Прихожая")
    living_light = Light("Гостиная")
    nest = Thermostat()
    tv = MediaCenter()

    hub = HomeCloud()

    # СЦЕНАРИЙ "Я ДОМА"

    i_am_home = MacroCommand([
        SmartCommand(hall_light.switch, {"status": "ВКЛ"}, "Включить свет в прихожей"),
        SmartCommand(nest.set_temp, {"t": 22}, "Комфортная температура"),
        SmartCommand(living_light.switch, {"status": "ВКЛ"}, "Уютный свет в зале")
    ], "Возвращение домой")

    hub.run(i_am_home)

    #СЦЕНАРИЙ "КИНОТЕАТР"
    cinema_mode = MacroCommand([
        SmartCommand(living_light.switch, {"status": "ВЫКЛ"}, "Выключить свет"),
        SmartCommand(tv.play_movie, {"title": "Интерстеллар"}, "Включить кино")
    ], "Вечерний просмотр")

    hub.run(cinema_mode)

    #СЦЕНАРИЙ "БЕЗОПАСНОСТЬ"

    leave_home_cmd = SmartCommand(hall_light.switch, {"status": "ВЫКЛ"}, "Автовыключение света")
    hub.schedule(leave_home_cmd, delay_seconds=2)