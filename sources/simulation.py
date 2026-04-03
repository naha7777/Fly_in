from sources.drones import Drone
from typing import Any


class Simulation:
    def __init__(self, max_moves: int, drones_lst: list[Drone],
                 zones: list[dict[str, Any]], paths: list[list[str]],
                 path_capacities: list[float],
                 connections: list[dict[str, Any]]) -> None:
        """Initialize the simulation with drones, zones, paths and capacty
           data"""
        self.max_moves = max_moves
        self.drones_lst = drones_lst
        self.zones = zones
        self.connections = connections
        self.paths = paths
        self.max_moves = max_moves
        self.drones_lst = drones_lst
        self.zones = zones
        self.paths = paths
        self.drones_in_simulation: list[Drone] = []
        self.dont_put_back: list[Drone] = []
        self.register_mouv: list[str] = []
        self.turns = 0
        self.drone_path: dict[str, int] = {}
        self.path_capacities = path_capacities
        self.drone_at_goal: list[Drone] = []
        self.count_goal = 0

    def drones_in_start_zone(self) -> None:
        """Place all drones in the start zone before the simulation begins"""
        start: str = str(self.zones[0].get("Name"))
        for drone in self.drones_lst:
            drone.add_drone_to_start(start)

    def get_drones_info(self) -> list[dict[str, Any]]:
        """Return a list of info dictionaries for all drones"""
        self.all_id_drones = []
        for drone in self.drones_lst:
            self.all_id_drones.append(drone.get_info())
        return self.all_id_drones

    def ft_print_datas_paths(self, actual_zones: list[str],
                             co_and_values: dict[str, int],
                             zo_and_values: dict[str, int],
                             paths: list[list[str]]) -> None:
        """Print zones'names and connections'names with number of drones and
           capacity if there is more than one path"""
        count_z: dict[str, int] = {}
        for item in actual_zones:
            count_z[item] = count_z.get(item, 0) + 1
        count_c: dict[str, int] = {}
        zones_actives: dict[Any, Any] = {}
        for path in paths:
            for i, step in enumerate(path):
                if step in actual_zones:
                    if step not in zones_actives:
                        zones_actives[step] = set()
                    if i > 0:
                        if "goal" in step:
                            self.count_goal += 1
                        connection = f"{path[i-1]}-{step}"
                        zones_actives[step].add(connection)
                        count_c[connection] = count_c.get(connection, 0) + 1
                    break
        for zone, connections in zones_actives.items():
            count_drones = count_z.get(zone, 0)
            max_drones = zo_and_values.get(zone)
            output = f"{zone}: {count_drones}/{max_drones}"
            if zone == "goal":
                output = f"{zone}: {self.count_goal}/{max_drones}"
            for co in connections:
                count_co = count_c.get(co, 0)
                max_link = co_and_values.get(co)
                output += f" {co}: {count_co}/{max_link}"
            print(output)

    def ft_print_datas(self, actual_z: list[str],
                       co_and_values: dict[str, int],
                       zo_and_values: dict[str, int], path: list[str]) -> None:
        """Print zones's names and connections's names with number of drones
           and capacity if there is only one path"""
        for i in range(0, len(actual_z)):
            zone_count = 0
            for zo in actual_z:
                if actual_z[i] == zo:
                    zone_count += 1
            if "-" in actual_z[i]:
                for co, v in co_and_values.items():
                    if actual_z[i] == co:
                        print(f"{actual_z[i]}: {zone_count}/{v}")
            else:
                for z, val in zo_and_values.items():
                    if actual_z[i] == z:
                        if "goal" in actual_z[i]:
                            self.count_goal += 1
                            print(f"{actual_z[i]}: {self.count_goal}/"
                                  f"{val}", end=", ")
                        else:
                            print(f"{actual_z[i]}: {zone_count}/"
                                  f"{val} ", end=", ")
                ind = 0
                while path[ind] != actual_z[i]:
                    ind += 1
                for c, value in co_and_values.items():
                    c_sp = c.split("-")
                    # if "-" in actual_z[i-1]:
                    #     pass
                    # if "-" not in path[ind-1]:
                    if c_sp[1] == actual_z[i] and c_sp[0] == path[ind-1]:
                        print(f"{path[ind-1]}-{actual_z[i]}: {zone_count}/"
                              f"{value}")
                    # else:
                    #     if c_sp[1] == actual_z[i] and c_sp[0] == path[ind-2]:
                    #         print(f"{path[ind-2]}-{actual_z[i]}: "\
                    #               f"{zone_count}/{value}")

    def simulate_turn(self, show_datas: bool) -> str | None:
        """Simulate one turn, move all active drones and return None when
           finished"""
        print()
        self.turns += 1
        drone_sent = 0
        path_index = 0

        actual_zones: list[str] = []
        co_and_values: dict[str, int] = {}
        zo_and_values: dict[str, int] = {}
        for co in self.connections:
            co_and_values[f"{co.get('Actual_Zone')}-"
                          f"{co.get('Zone_to_move_on')}"] = \
                            co.get("Max_link_capacity", 0)
        for zo in self.zones:
            zo_and_values[str(zo.get("Name"))] = zo.get("Max_drones", 0)

        if len(self.paths) == 1:
            for drone in self.drones_in_simulation:
                self.register_mouv.append(f"{drone.ID}-{drone.zone}")
                path = self.paths[0]
                i = 0
                while path[i] != drone.zone:
                    i += 1
                if i + 1 < len(path):
                    drone.move_drone(path[i+1])

            for drone in self.drones_in_simulation:
                if drone not in self.drone_at_goal:
                    if drone.zone != self.zones[0].get("Name"):
                        print(f"{drone.ID}-{drone.zone}", end=" ")
                        if show_datas:
                            actual_zones.append(str(drone.zone))
                    if drone.zone == self.zones[-1].get("Name"):
                        self.drone_at_goal.append(drone)
                else:
                    pass

            for d in self.drones_lst:
                if d not in self.dont_put_back:
                    if drone_sent < self.max_moves:
                        self.drones_in_simulation.append(d)
                        self.dont_put_back.append(d)
                        drone_sent += 1
                    else:
                        drone_sent = 0
                        break

            finished = sum(1 for d in self.drones_lst
                           if d.zone == self.zones[-1].get("Name"))

            if show_datas and len(actual_zones) != 0:
                print()
                self.ft_print_datas(actual_zones, co_and_values, zo_and_values,
                                    path)

            if finished == len(self.drones_lst):
                return None
            print()
            return (f"\nTurn {self.turns}")

        else:
            actual_ids = []
            for drone in self.drones_in_simulation:
                path = self.paths[self.drone_path[drone.ID]]
                y = 0
                while path[y] != drone.zone:
                    y += 1
                if y + 1 <= len(path) - 1:
                    drone.move_drone(path[y+1])

            for drone in self.drones_in_simulation:
                if drone.zone != self.zones[0].get("Name") \
                   and drone.zone != self.zones[-1].get("Name"):
                    print(f"{drone.ID}-{drone.zone}", end=" ")
                    if show_datas:
                        actual_zones.append(str(drone.zone))

            for drone in self.drones_in_simulation:
                if drone.zone == self.zones[-1].get("Name"):
                    print(f"{drone.ID}-{drone.zone}", end=" ")
                    if show_datas:
                        actual_zones.append(str(drone.zone))
                        actual_ids.append(drone.ID)

            for drone in self.drones_in_simulation[:]:
                if drone.zone == self.zones[-1].get("Name"):
                    self.drones_in_simulation.remove(drone)
                    del self.drone_path[drone.ID]

            for d in self.drones_lst:
                if d not in self.dont_put_back:
                    if drone_sent < self.max_moves:
                        found = False
                        for pi in range(len(self.paths)):
                            drones_on_path = sum(1 for drone in
                                                 self.drones_in_simulation
                                                 if
                                                 self.drone_path.get(drone.ID)
                                                 == pi)
                            if drones_on_path < self.path_capacities[pi]:
                                path_index = pi
                                found = True
                                break
                        if not found:
                            break
                        self.drones_in_simulation.append(d)
                        self.dont_put_back.append(d)
                        self.drone_path[d.ID] = path_index
                        drone_sent += 1
                    else:
                        break
        finished = sum(1 for d in self.drones_lst if d.zone ==
                       self.zones[-1].get("Name"))
        if show_datas and len(actual_zones) != 0:
            print()
            self.ft_print_datas_paths(actual_zones, co_and_values,
                                      zo_and_values, self.paths)
        if finished == len(self.drones_lst):
            return None
        print()
        return (f"\nTurn {self.turns}")
