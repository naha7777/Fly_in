# from sources.drones import Drones
from sources.zones import Zone
from typing import Any
from sources.connections import Connection
from sources.algo import EdmondsKarp


class Manager:
    zones_lst: list[Zone] = []
    connection_lst: list[Connection] = []

    def __init__(self, map_valid: dict[str, Any]) -> None:
        self.map_valid = map_valid
        self.nb_drones = self.map_valid["nb_drones"]
        self.zones = {}
        for k, v in self.map_valid.items():
            if k != "nb_drones" and k != "connections":
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
        return self.zones_lst

    def get_zo_infos(self) -> None:
        self.all_about_zones = []
        for zone in self.zones_lst:
            self.all_about_zones.append(zone.get_info())

    def create_connections(self) -> None:
        self.co_name = "connection"
        self.actual_zone = "start"
        self.zone_to_move_on = "end"
        self.max_link_capacity = 0
        self.connections = {}
        for k, v in self.map_valid.items():
            if k == "connections":
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
                    self.max_link_capacity =\
                        int(find_max_link_value[1].rstrip("]"))
                for zone in self.all_about_zones:
                    if self.actual_zone == zone.get("Name")\
                       or self.zone_to_move_on == zone.get("Name"):
                        if zone.get("Type_Zone") == "blocked":
                            self.max_link_capacity = 0
                self.new_connection = Connection(self.co_name,
                                                 self.actual_zone,
                                                 self.zone_to_move_on,
                                                 self.max_link_capacity)
                self.connection_lst.append(self.new_connection)

    def get_co_infos(self) -> None:
        self.all_about_connections = []
        for connection in self.connection_lst:
            self.all_about_connections.append(connection.get_info())

    def create_matrice(self) -> tuple[list[list[int]], int, int]:
        self.matrice = []
        size = (len(self.all_about_zones)) * 2
        for i in range(size):
            self.matrice.append([0] * size)
        self.raw_col: dict[str, dict[str, int]] = {}
        i = 0
        self.s: int = i
        for zone in self.all_about_zones:
            self.raw_col[str(zone.get("Name"))] = {"in": i, "out": i+1}
            i += 2
        self.e: int = i - 1
        for zone in self.all_about_zones:
            zone_in = self.raw_col[str(zone.get("Name"))]["in"]
            zone_out = self.raw_col[str(zone.get("Name"))]["out"]
            self.matrice[zone_in][zone_out] = int(zone.get("Max_drones") or 1)
            for connection in self.all_about_connections:
                zone_A_in =\
                    self.raw_col[str(connection.get("Actual_Zone"))]["in"]
                zone_A_out =\
                    self.raw_col[str(connection.get("Actual_Zone"))]["out"]
                zone_B_in =\
                    self.raw_col[str(connection.get("Zone_to_move_on"))]["in"]
                zone_B_out =\
                    self.raw_col[str(connection.get("Zone_to_move_on"))]["out"]
                self.matrice[zone_A_out][zone_B_in] =\
                    int(connection.get("Max_link_capacity") or 1)
                self.matrice[zone_B_out][zone_A_in] =\
                    int(connection.get("Max_link_capacity") or 1)
        return self.matrice, self.s, self.e

    def create_algo(self, algo: EdmondsKarp) -> tuple[list[list[int]], int]:
        F, max_drones_mouv = algo.create_matrice_F()
        return F, max_drones_mouv

    def extract_paths(self, F: list[list[int]]) -> list[str]:
        self.paths_found = []
        coor_path = self.bfs_extract(F, self.s, self.e)
        while coor_path is not None:
            flow = min(F[u][v] for u, v in coor_path)
            self.paths_found.append(coor_path)
            for u, v in coor_path:
                F[u][v] -= flow
            coor_path = self.bfs_extract(F, self.s, self.e)
        self.translate_path = []
        for k, val in self.raw_col.items():
            for list in self.paths_found:
                for tup in list:
                    x, y = tup
                    if x in val.values() and y in val.values():
                        self.translate_path.append(k)
                    elif y in val.values():
                        self.translate_path.append(k)
                    elif x in val.values():
                        self.translate_path.append(f"{k}-")
        self.path = []
        remove = False
        save_string = None
        for string in self.translate_path:
            if not remove:
                if save_string is not None:
                    if "-" in save_string:
                        self.path.append(f"{save_string}{string}")
                    else:
                        self.path.append(string)
                else:
                    self.path.append(string)
                remove = True
            elif remove:
                if "-" in string:
                    save_string = string
                    remove = False
                else:
                    self.path.append(string)
        return (self.path)

    def bfs_extract(self, F: list[list[int]], s: int,
                    e: int) -> list[tuple[int, int]] | None:
        queue = [s]
        paths: dict[int, list[tuple[int, int]]] = {s: []}
        if s == e:
            return paths[s]
        while queue:
            u = queue.pop(0)
            for v in range(len(F)):
                if F[u][v] > 0 and v not in paths:
                    paths[v] = paths[u] + [(u, v)]
                    if v == e:
                        return paths[v]
                    queue.append(v)
        return None

    # def create_drones(self) -> None:
    #     pass
