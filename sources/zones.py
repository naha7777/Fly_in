from typing import Any


class Zone:
    def __init__(self, name: str, type_zone: str,
                 color: str, max_drones: int, coordinates: tuple[int]) -> None:
        self.name = name
        self.type_zone = type_zone
        self.color = color
        self.max_drones = max_drones
        self.coordinates = coordinates

    def get_info(self) -> dict[str, Any]:
        return ({"Name": self.name, "Type_Zone": self.type_zone,
                 "Color": self.color,
                 "Max_drones": self.max_drones,
                 "Coordinates": self.coordinates})
