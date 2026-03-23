from typing import Any


class Drone:
    def __init__(self, ID: int, zone: str | None) -> None:
        self.ID = f"D{ID}"
        self.zone = zone

    def add_drone_to_start(self, start_name: str) -> None:
        self.zone = start_name

    def move_drone(self, next_zone: str) -> None:
        self.zone = next_zone

    def get_info(self) -> dict[str, Any]:
        return ({f"Drone{self.ID}'s ID": self.ID, "Zone": self.zone})
