from sources.drones import Drone


class Simulation:
    def __init__(self, max_mouv: int, drones_lst: list[Drone],
                 zones: list, paths: list) -> None:
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

        if len(self.paths) == 1:
            for d in self.drones_lst:
                if d not in self.dont_put_back:
                    if drone_sent < self.max_mouv:
                        self.drones_in_simulation.append(d)
                        self.dont_put_back.append(d)
                        drone_sent += 1
                    else:
                        drone_sent = 0
                        break

            for drone in self.drones_in_simulation[:]:
                if drone.zone == self.zones[-1].get("Name"):
                    print(f"{drone.ID}-{drone.zone}", end=" ")
                    self.drones_in_simulation.remove(drone)

            for drone in self.drones_in_simulation:
                self.register_mouv.append(f"{drone.ID}-{drone.zone}")
                if drone.zone != self.zones[0].get("Name"):
                    print(f"{drone.ID}-{drone.zone}", end=" ")

                #trouver la zone du drone dans le path
                for list in self.paths:
                    i = 0
                    while list[i] != drone.zone:
                        i += 1

                #bouger le drone dans la zone suivante du chemin
                for list in self.paths:
                    if max_drones != len(self.drones_in_simulation):
                        if i == len(self.paths) - 1:
                            i = 0
                        drone.move_drone(list[i+2])
                        max_drones += 1

            #check si tlm est arrive a goal
            finished = sum(1 for d in self.drones_lst if d.zone == self.zones[-1].get("Name"))
            if finished == len(self.drones_lst):
                print(f"\nTurn {self.turns}")
                for drone in self.drones_in_simulation:
                    print(f"{drone.ID}-{drone.zone}", end=" ")
                return None
            return(f"\nTurn {self.turns}")

        # else:


