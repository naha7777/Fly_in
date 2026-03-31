from typing import Any


class Drone:
    def __init__(self, ID: int, zone: str | None) -> None:
        """Initialize Drone with an id and a zone"""
        self.ID = f"D{ID}"
        self.zone = zone

    def add_drone_to_start(self, start_name: str) -> None:
        """Change the zone None to the start zone"""
        self.zone = start_name

    def move_drone(self, next_zone: str) -> None:
        """Move a drone from actual zone to the next one"""
        self.zone = next_zone

    def get_info(self) -> dict[str, Any]:
        """Return a dict with all informations about a drone"""
        return ({f"Drone{self.ID}'s ID": self.ID, "Zone": self.zone})
