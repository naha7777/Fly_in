# from sources.drones import Drones
from sources.zones import Zone
from typing import Any


class Manager:
    zones_lst: list[Zone] = []

    def __init__(self, map_valid: dict[str, Any]) -> None:
        self.map_valid = map_valid
        self.nb_drones = self.map_valid["nb_drones"]
        if "connections" in self.map_valid:
            self.co_names = []
            self.co_metadatas = []
            for k, v in map_valid["connections"].items():
                parts = v.split(" ")
                self.co_names.append(parts[0])
                if "[" in v:
                    self.co_metadatas.append(v.split("[")[1].rstrip("]"))
                else:
                    self.co_metadatas.append("max_link_capacity=1")
        self.zones = {}
        for k, v in self.map_valid.items():
            if k != "nb_drones" and k != "connections":
                self.zones[k] = v

    def create_zones(self) -> None:
        for k, v in self.zones.items():
            self.name: str | Any = None
            self.metadt: str | Any = None
            self.color: str = "white"
            self.type: str = "normal"
            self.max_drones: int = 1
            if k != "hubs":
                split_value = v.split(" ")
                metadatas = v.split("[")
                self.name = split_value[0]
                if len(split_value) >= 4:
                    self.metadt = metadatas[1]
                else:
                    self.metadt = "[color=white zone=normal max_drones=1]"
                separate_data = self.metadt.split(" ")
                for data in separate_data:
                    split_data = data.split("=")
                    if "color" in split_data[0]:
                        self.color = split_data[1].rstrip("]")
                    if "zone" in split_data[0]:
                        self.type = split_data[1].rstrip("]")
                    if "max_drones" in split_data[0]:
                        self.max_drones = int(split_data[1].rstrip("]"))
                    if self.color is None:
                        self.color = "white"
                    if self.type is None:
                        self.type = "normal"
                    if self.max_drones == 0:
                        self.max_drones = 1
                self.new_zone = Zone(self.name, self.type, self.color,
                                     self.max_drones)
                self.zones_lst.append(self.new_zone)
            else:
                for key, value in v.items():
                    self.name = key
                    split_value = value.split(" ")
                    metadatas = value.split("[")
                    self.name = split_value[0]
                    if len(split_value) >= 4:
                        self.metadt = metadatas[1]
                    else:
                        self.metadt = "[color=white zone=normal max_drones=1]"
                    separate_data = self.metadt.split(" ")
                    for data in separate_data:
                        split_data = data.split("=")
                        if "color" in split_data[0]:
                            self.color = split_data[1].rstrip("]")
                        if "zone" in split_data[0]:
                            self.type = split_data[1].rstrip("]")
                        if "max_drones" in split_data[0]:
                            self.max_drones = int(split_data[1].rstrip("]"))
                        if self.color is None:
                            self.color = "white"
                        if self.type is None:
                            self.type = "normal"
                        if self.max_drones == 0:
                            self.max_drones = 1
                    self.new_zone = Zone(self.name, self.type, self.color,
                                         self.max_drones)
                    self.zones_lst.append(self.new_zone)

    def create_drones(self) -> None:
        pass
