# from sources.drones import Drones
from sources.zones import Zone
from typing import Any
from sources.connections import Connection


class Manager:
    zones_lst: list[Zone] = []
    connection_lst: list = []

    def __init__(self, map_valid: dict[str, Any]) -> None:
        self.map_valid = map_valid
        self.nb_drones = self.map_valid["nb_drones"]
        self.zones = {}
        for k, v in self.map_valid.items():
            if k != "nb_drones" and k!= "connections":
                self.zones[k] = v

    def create_zones(self) -> list[Zone]:
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
                if k == "start_hub" or k == "end_hub":
                    self.max_drones = self.nb_drones
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

    def create_connections(self) -> None:
        self.co_name = "connection"
        self.actual_zone = "start"
        self.zone_to_move_on = "end"
        self.max_link_capacity = 1
        self.connections = {}
        for k, v in self.map_valid.items():
            if k== "connections":
                self.connections[k] = v
        for k, v in self.connections.items():
            for key, value in v.items():
                self.co_name = key
                split_co = value.split("-")
                self.actual_zone = split_co[0]
                if "[" not in split_co[1]:
                    self.zone_to_move_on = split_co[1]
                    self.max_link_capacity = 1
                else:
                    find_metadatas = split_co[1].split("[")
                    self.zone_to_move_on = find_metadatas[0].rstrip(" ")
                    find_max_link_value = find_metadatas[1].split("=")
                    self.max_link_capacity = int(find_max_link_value[1].rstrip("]"))
                self.new_connection = Connection(self.co_name,
                                                 self.actual_zone,
                                                 self.zone_to_move_on,
                                                 self.max_link_capacity)
                self.connection_lst.append(self.new_connection)

    def get_co_infos(self) -> None:
        self.all_about_connections = []
        for connection in self.connection_lst:
            self.all_about_connections.append(connection.get_info())

    def get_zo_infos(self) -> None:
        self.all_about_zones = []
        for zone in self.zones_lst:
            self.all_about_zones.append(zone.get_info())

    def create_matrice(self) -> list[list[int]]:
        self.matrice = []
        size = (len(self.all_about_zones)) * 2
        for i in range(size):
            self.matrice.append([0] * size)
        raw_col = {}
        i = 0
        for zone in self.all_about_zones:
            raw_col[zone.get("Name")] = {"in": i, "out": i+1}
            i += 2
        for zone in self.all_about_zones:
            zone_in = raw_col[zone.get("Name")]["in"]
            zone_out = raw_col[zone.get("Name")]["out"]
            self.matrice[zone_in][zone_out] = zone.get("Max_drones")
            for connection in self.all_about_connections:
                zone_A_in = raw_col[connection.get("Actual_Zone")]["in"]
                zone_A_out = raw_col[connection.get("Actual_Zone")]["out"]
                zone_B_in = raw_col[connection.get("Zone_to_move_on")]["in"]
                zone_B_out = raw_col[connection.get("Zone_to_move_on")]["out"]
                self.matrice[zone_A_out][zone_B_in] = connection.get("Max_link_capacity")
                self.matrice[zone_B_out][zone_A_in] = connection.get("Max_link_capacity")
        print(self.matrice)
        return self.matrice


    # def create_drones(self) -> None:
    #     pass
