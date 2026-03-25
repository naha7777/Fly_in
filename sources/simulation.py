from sources.drones import Drone


class Simulation:
    def __init__(self, max_mouv: int, drones_lst: list[Drone],
                 zones: list, paths: list, path_capacities: list[int]) -> None:
        self.max_mouv = max_mouv
        self.drones_lst = drones_lst
        self.zones = zones
        self.paths = paths
        self.max_mouv = max_mouv
        self.drones_lst = drones_lst
        self.zones = zones
        self.paths = paths
        self.drones_in_simulation = []
        self.dont_put_back = []
        self.register_mouv = []
        self.turns = 0
        self.drone_path = {}
        self.path_capacities = path_capacities

    def drones_in_start_zone(self) -> None:
        start = self.zones[0].get("Name")
        for drone in self.drones_lst:
            drone.add_drone_to_start(start)

    def get_drones_info(self) -> list:
        self.all_id_drones = []
        for drone in self.drones_lst:
            self.all_id_drones.append(drone.get_info())
        return self.all_id_drones

    def simulate_turn(self) -> int | None:
        self.turns += 1
        max_drones = 0
        drone_sent = 0
        path_index = 0

        if len(self.paths) == 1:
            for drone in self.drones_in_simulation[:]:
                if drone.zone == self.zones[-1].get("Name"):
                    print(f"{drone.ID}-{drone.zone}", end=" ")
                    self.drones_in_simulation.remove(drone)
            for d in self.drones_lst:
                if d not in self.dont_put_back:
                    if drone_sent < self.max_mouv:
                        self.drones_in_simulation.append(d)
                        self.dont_put_back.append(d)
                        drone_sent += 1
                    else:
                        drone_sent = 0
                        break
            for drone in self.drones_in_simulation:
                self.register_mouv.append(f"{drone.ID}-{drone.zone}")
                if drone.zone != self.zones[0].get("Name"):
                    print(f"{drone.ID}-{drone.zone}", end=" ")
                for p in self.paths:
                    i = 0
                    while p[i] != drone.zone:
                        i += 1
                for p in self.paths:
                    if max_drones != len(self.drones_in_simulation):
                        if i + 1 < len(p):
                            drone.move_drone(p[i+1])
                        max_drones += 1
            finished = sum(1 for d in self.drones_lst
                           if d.zone == self.zones[-1].get("Name"))
            if finished == len(self.drones_lst):
                print(f"\nTurn {self.turns}")
                print(f"{drone.ID}-{drone.zone}", end=" ")
                return None
            return(f"\nTurn {self.turns}")

        else:
            for drone in self.drones_in_simulation:
                path = self.paths[self.drone_path[drone.ID]]
                y = 0
                while path[y] != drone.zone:
                    y += 1
                # if y + 2 <= len(path) - 1:
                #     drone.move_drone(path[y+2])
                if y + 1 <= len(path) - 1:
                    drone.move_drone(path[y+1])
                if drone.zone != self.zones[0].get("Name") \
                    and drone.zone != self.zones[-1].get("Name"):
                    print(f"{drone.ID}-{drone.zone}", end=" ")
            for drone in self.drones_in_simulation[:]:
                if drone.zone == self.zones[-1].get("Name"):
                    print(f"{drone.ID}-{drone.zone}", end=" ")
                    self.drones_in_simulation.remove(drone)
                    del self.drone_path[drone.ID]
            for d in self.drones_lst:
                if d not in self.dont_put_back:
                    if drone_sent < self.max_mouv:
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
        return(f"\nTurn {self.turns}")

