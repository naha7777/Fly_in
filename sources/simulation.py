from sources.drones import Drone


class Simulation:
    turns = 0
    def __init__(self, max_mouv: int, drones_lst: list[Drone],
                 zones: list, paths: list) -> None:
        self.max_mouv = max_mouv
        self.drones_lst = drones_lst
        self.zones = zones
        self.paths = paths

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
        drone_finish = 0
        for drone in self.drones_lst:
            if drone.zone == self.zones[len(self.zones) - 1].get("Name"):
                drone_finish += 1
            i = 0
            while self.paths[i] != drone.zone:
                i += 1
            if max_drones != self.max_mouv:
                if i == len(self.paths) - 1:
                    i = 0
                drone.move_drone(self.paths[i+2])
                max_drones += 1
        if drone_finish == len(self.drones_lst):
                    return None
        return(f"Turn {self.turns} -> {drone.ID}-{drone.zone}\n")
