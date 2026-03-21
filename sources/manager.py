# from sources.drones import Drones
# from sources.zones import Zones
from typing import Any


class Manager:
    def __init__(self, map_valid: dict[str, Any]) -> None:
        self.map_valid = map_valid
        self.nb_drones = self.map_valid["nb_drones"]
        self.start_hub = self.map_valid["start_hub"]
        self.start_name = self.start_hub.split(" ")[0]
        self.end_hub = self.map_valid["end_hub"]
        self.end_name = self.end_hub.split(" ")[0]
        if "[" in self.start_hub:
            self.start_metadata = self.start_hub.split("[")[1].rstrip("]")
        if "[" in self.end_hub:
            self.end_metadata = self.end_hub.split("[")[1].rstrip("]")
        if "hubs" in self.map_valid:
            self.hubs_names = []
            self.hubs_metadatas = []
            for k, v in map_valid["hubs"].items():
                parts = v.split(" ")
                self.hubs_names.append(parts[0])
                if "[" in v:
                    self.hubs_metadatas.append(v.split("[")[1].rstrip("]"))
                else:
                    self.hubs_metadatas.append("no metada for this one")
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

    def create_zones(self) -> None:
        pass

    def create_drones(self) -> None:
        pass
