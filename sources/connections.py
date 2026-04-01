from typing import Any


class Connection:
    def __init__(self, name: str, actual_zone: str, zone_to_move_on: str,
                 max_link_capacity: int) -> None:
        """Initialize a connection between two zones with its capacity"""
        self.name = name
        self.actual_zone = actual_zone
        self.zone_to_move_on = zone_to_move_on
        self.max_link_capacity = max_link_capacity

    def get_info(self) -> dict[str, Any]:
        """Return a dictionary containing all connection attributes"""
        return ({"Name": self.name, "Actual_Zone": self.actual_zone,
                 "Zone_to_move_on": self.zone_to_move_on,
                 "Max_link_capacity": self.max_link_capacity})
