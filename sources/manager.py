from sources.drones import Drone
from sources.zones import Zone
from typing import Any
from sources.connections import Connection
from sources.algo import EdmondsKarp
from sources.simulation import Simulation
from sources.visual import Visual
import arcade
from contextlib import redirect_stdout


class Manager:
    def __init__(self, map_valid: dict[str, Any]) -> None:
        """Initialize the Manager with a validated map configuration"""
        self.zones_lst: list[Zone] = []
        self.connection_lst: list[Connection] = []
        self.drones_lst: list[Drone] = []
        self.map_valid = map_valid
        self.nb_drones = self.map_valid["nb_drones"]
        self.zones = {}
        self.path: list[list[str]] = []
        for k, v in self.map_valid.items():
            if k != "nb_drones" and k != "connections":
                self.zones[k] = v

    def create_zones(self) -> list[Zone]:
        """Parse map data and instantiate all Zone objects"""
        for k, v in self.zones.items():
            self.name: str | Any = None
            self.metadt: str | Any = None
            self.color: str = "black"
            self.type: str = "normal"
            self.max_drones: int = 1
            self.coordinates: tuple[int, int] = (0, 0)
            if k != "hubs":
                split_value = v.split(" ")
                metadatas = v.split("[")
                self.name = split_value[0]
                x, y = split_value[1], split_value[2]
                self.coordinates = int(x), int(y)
                if len(split_value) >= 4:
                    self.metadt = metadatas[1]
                else:
                    self.metadt = "[color=black zone=normal max_drones=1]"
                separate_data = self.metadt.split(" ")
                for data in separate_data:
                    split_data = data.split("=")
                    meta_val = split_data[1]
                    if "color" in split_data[0]:
                        self.color = meta_val.rstrip("]")
                    if "zone" in split_data[0]:
                        self.type = meta_val.rstrip("]")
                    if "max_drones" in split_data[0]:
                        self.max_drones = int(meta_val.rstrip("]"))
                    elif split_data[0] == "zone" and meta_val == "blocked":
                        self.type = meta_val
                        self.max_drones = 0
                if k == "start_hub" or k == "end_hub":
                    self.max_drones = self.nb_drones
                self.new_zone = Zone(self.name, self.type, self.color,
                                     self.max_drones, self.coordinates)
                self.zones_lst.append(self.new_zone)
            else:
                for key, value in v.items():
                    name: str | Any = None
                    metadt: str | Any = None
                    color: str = "black"
                    type: str = "normal"
                    max_drones: int = 1
                    name = key
                    split_value = value.split(" ")
                    metadatas = value.split("[")
                    name = split_value[0]
                    x, y = split_value[1], split_value[2]
                    coordinates = int(x), int(y)
                    if len(split_value) >= 4:
                        metadt = metadatas[1]
                    else:
                        metadt = "[color=black zone=normal max_drones=1]"
                    separate_data = metadt.split(" ")
                    for data in separate_data:
                        data = data.rstrip("]")
                        split_data = data.split("=")
                        if split_data[0] == "color":
                            color = split_data[1]
                        if split_data[0] == "zone":
                            type = split_data[1]
                        if split_data[0] == "max_drones":
                            max_drones = int(split_data[1])
                        if split_data[0] == "zone"\
                           and split_data[1] == "blocked":
                            type = split_data[1]
                            max_drones = 0
                    self.new_zone = Zone(name, type, color,
                                         max_drones, coordinates)
                    self.zones_lst.append(self.new_zone)
        return self.zones_lst

    def get_zo_infos(self) -> None:
        """Populate all_about_zones with info dicts from each zone"""
        self.all_about_zones = []
        for zone in self.zones_lst:
            self.all_about_zones.append(zone.get_info())

    def create_connections(self) -> None:
        """Parse map data and instantiate all Connection objects"""
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
        """
        Populate all_about_connections with info dicts from each connection
        """
        self.all_about_connections = []
        for connection in self.connection_lst:
            self.all_about_connections.append(connection.get_info())

    def create_matrice(self) -> tuple[list[list[int]], int, int]:
        """Build the capacity matrix for the flow network and return it
           with source and sink indices"""
        self.matrice = []
        size = (len(self.all_about_zones)) * 2
        for i in range(size):
            self.matrice.append([0] * size)
        self.raw_col = {}
        i = 0
        self.s = i
        for zone in self.all_about_zones:
            self.raw_col[str(zone.get("Name"))] = {"in": i, "out": i+1}
            i += 2
        self.e = i - 1
        for zone in self.all_about_zones:
            zone_in = self.raw_col[str(zone.get("Name"))]["in"]
            zone_out = self.raw_col[str(zone.get("Name"))]["out"]
            self.matrice[zone_in][zone_out] = int(zone.get("Max_drones") or 0)
        for connection in self.all_about_connections:
            zone_A_out =\
                self.raw_col[str(connection.get("Actual_Zone"))]["out"]
            zone_B_in =\
                self.raw_col[str(connection.get("Zone_to_move_on"))]["in"]
            capacity = int(connection.get("Max_link_capacity") or 0)
            self.matrice[zone_A_out][zone_B_in] = capacity
        return self.matrice, self.s, self.e

    def create_algo(self, algo: EdmondsKarp) -> tuple[list[list[int]], int]:
        """Run Edmonds-Karp on the capacity matrix and return the flow
           matrix and max drone movements"""
        priority_indices = set()
        for zone in self.all_about_zones:
            if zone.get("Type_Zone") == "priority":
                zone_name = zone.get("Name")
                priority_indices.add(self.raw_col[str(zone_name)]["in"])
                priority_indices.add(self.raw_col[str(zone_name)]["out"])
        algo.priority = priority_indices
        F, max_drones_mouv = algo.create_matrice_F()
        return F, max_drones_mouv

    def restriction(self, path: list[list[str]]) -> list[list[str]]:
        """Insert restriction markers into paths that pass through
           restricted zones"""
        self.restricteds = []
        steps = []
        for zone in self.all_about_zones:
            if zone.get("Type_Zone") == "restricted":
                self.restricteds.append(zone.get("Name"))
        self.separate_paths = []
        i = 0
        for p in path:
            self.path_restricted = []
            for step in p:
                steps.append(step)
                if step in self.restricteds:
                    self.path_restricted.append(f"{steps[i-1]}-{step}")
                    self.path_restricted.append(step)
                else:
                    self.path_restricted.append(step)
                i += 1
            self.separate_paths.append(self.path_restricted)
        return self.separate_paths

    def extract_paths(self, F: list[list[int]]) -> list[list[str]]:
        """Extract all individual paths from the flow matrix and translate
           them to zone name sequences"""
        local_paths_found: list[list[tuple[int, int]]] = []
        coor_path = self.bfs_extract(F, self.s, self.e)
        while coor_path is not None:
            flow = min(F[u][v] for u, v in coor_path)
            local_paths_found.append(coor_path)
            for u, v in coor_path:
                F[u][v] -= flow
            coor_path = self.bfs_extract(F, self.s, self.e)

        translate_path: list[list[str]] = []

        for p in local_paths_found:
            one_path: list[str] = []
            for tup in p:
                x, y = tup
                for k, val in self.raw_col.items():
                    if x == val["in"] and y == val["out"]:
                        one_path.append(str(k))
                    elif y == val["out"]:
                        one_path.append(str(k))
                    elif x == val["in"]:
                        one_path.append(f"{str(k)}-")
            translate_path.append(one_path)

        path: list[list[str]] = []
        remove = False
        save_string: str | None = None
        for tp in translate_path:
            lst: list[str] = []
            for stri in tp:
                string = str(stri)
                if not remove:
                    if save_string is not None:
                        if "-" in save_string:
                            lst.append(f"{save_string}{string}")
                        else:
                            lst.append(string)
                    else:
                        lst.append(string)
                    remove = True
                elif remove:
                    if "-" in string:
                        save_string = string
                        remove = False
                    else:
                        lst.append(string)
                if string == self.all_about_zones[-1].get("Name"):
                    break
            path.append(lst)
        self.path = self.restriction(path)
        return self.path

    def bfs_extract(self, F: list[list[int]], s: int,
                    e: int) -> list[tuple[int, int]] | None:
        """Find one augmenting path from s to e in F using BFS, or
           return None if none exists"""
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

    def create_drones(self) -> None:
        """Instantiate all drone objects based on the configured drone
           count"""
        for i in range(1, self.nb_drones + 1):
            new_drone = Drone(i, None)
            self.drones_lst.append(new_drone)

    def simulate(self, max_mouv: int, show_datas: bool) -> None:
        """Run the full simulation and write the turn-by-turn output to
           output.txt"""
        self.max_mouv = max_mouv
        path_capacities = []
        for path in self.path:
            inf = float('inf')
            i = 0
            for co in self.all_about_connections:
                if path[i] == co.get("Actual_Zone")\
                     and path[i+1] == co.get("Zone_to_move_on"):
                    max_lk = int(co.get("Max_link_capacity") or 1)
                    inf = min(inf, max_lk)
                    i += 1
            for step in path:
                if "-" not in step:
                    for zone in self.all_about_zones:
                        if zone.get("Name") == step:
                            max_dr = int(zone.get("Max_drones") or 1)
                            inf = min(inf, max_dr)
                else:
                    parts = step.split("-")
                    for co in self.all_about_connections:
                        if co.get("Actual_Zone") == parts[0] \
                           and co.get("Zone_to_move_on") == parts[1]:
                            max_dr = int(co.get("Max_link_capacity") or 1)
                            inf = min(inf, max_dr)
            path_capacities.append(inf)

        paired = list(zip(self.path, path_capacities))
        paired.sort(key=lambda x: len(x[0]))
        self.path = [p[0] for p in paired]
        self.path_capacities = [p[1] for p in paired]

        simulator = Simulation(self.max_mouv, self.drones_lst,
                               self.all_about_zones, self.path,
                               self.path_capacities,
                               self.all_about_connections)
        simulator.drones_in_start_zone()
        simulator.get_drones_info()

        res: Any = 0
        tt_turn = -1
        with open("output.txt", "w") as f:
            with redirect_stdout(f):
                while res is not None:
                    tt_turn += 1
                    res = simulator.simulate_turn(show_datas)
        print(f"Total turns: {tt_turn}")

    def animate(self) -> None:
        """Launch the arcade window to visually animate the simulation"""
        simulator = Simulation(self.max_mouv, self.drones_lst,
                               self.all_about_zones,
                               self.path, self.path_capacities,
                               self.all_about_connections)
        all_drones = simulator.get_drones_info()
        window = Visual(self.all_about_zones, self.all_about_connections,
                        all_drones)
        window.setup()
        arcade.run()
