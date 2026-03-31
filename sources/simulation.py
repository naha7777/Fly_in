from sources.drones import Drone
from typing import Any


class Simulation:
    def __init__(self, max_moves: int, drones_lst: list[Drone],
                 zones: list[dict[str, Any]], paths: list[list[str]],
                 path_capacities: list[float]) -> None:
        """Initialize Simulation with a maximum number of moves, informations
           about drones, zones, paths and path capacities."""
        self.max_moves = max_moves
        self.drones_lst = drones_lst
        self.zones = zones
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

    def drones_in_start_zone(self) -> None:
        """Call the method putting all drones in start zone"""
        start: str = str(self.zones[0].get("Name"))
        for drone in self.drones_lst:
            drone.add_drone_to_start(start)

    def get_drones_info(self) -> list[dict[str, Any]]:
        """Put all informations about drones on a list and return it"""
        self.all_id_drones = []
        for drone in self.drones_lst:
            self.all_id_drones.append(drone.get_info())
        return self.all_id_drones

    def simulate_turn(self) -> str | None:
        """Simulate a turn : count the number of turns and move the drones
           following the path/s, write all drones movements in one line"""
        self.turns += 1
        drone_sent = 0
        path_index = 0

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
                if drone.zone != self.zones[0].get("Name"):
                    print(f"{drone.ID}-{drone.zone}", end=" ")

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
            if finished == len(self.drones_lst):
                print()
                return None
            print()
            return (f"\nTurn {self.turns}")

        else:
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

            for drone in self.drones_in_simulation:
                if drone.zone == self.zones[-1].get("Name"):
                    print(f"{drone.ID}-{drone.zone}", end=" ")

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
        if finished == len(self.drones_lst):
            return None
        print()
        return (f"\nTurn {self.turns}")
