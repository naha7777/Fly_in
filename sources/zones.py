class Zone:
    def __init__(self, name: str, type_zone: str,
                 color: str, max_drones: int) -> None:
        self.name = name
        self.type_zone = type_zone
        self.color = color
        self.max_drones = max_drones
