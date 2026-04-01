from typing import Any


class Drone:
    def __init__(self, ID: int, zone: str | None) -> None:
        """Initialize a drone with an id and its startting zone"""
        self.ID = f"D{ID}"
        self.zone = zone

    def add_drone_to_start(self, start_name: str) -> None:
        """Place the drone in the start zone"""
        self.zone = start_name

    def move_drone(self, next_zone: str) -> None:
        """Move the drone to the next zone"""
        self.zone = next_zone

    def get_info(self) -> dict[str, Any]:
        """Return a dictionary containing the drone's ID and current zone"""
        return ({f"Drone{self.ID}'s ID": self.ID, "Zone": self.zone})
