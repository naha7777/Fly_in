import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Fly_in Visual"
ZONES = 20
DRONES = 10


class Visual(arcade.Window):
    def __init__(self, zones, connections, drones):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.WHITE)
        self.time_elapsed = 0
        self.move_delay = 5.0
        self.paused = False
        self.pause_timer = 0
        self.pause_duration = 0

        self.turn = 0

        self.drone_x_position = 0
        self.drone_x_pixels_per_second = 0

        self.zones = zones
        self.zone_lst = arcade.SpriteList()

        self.camera = arcade.camera.Camera2D()
        self.camera.position = (0, 0)
        self.gui_camera = arcade.camera.Camera2D()

        self.texts_to_draw = []
        self.draw_connections = []
        self.draw_max_drones = []

        self.connections = connections

        self.drones = drones
        self.drone_lst = arcade.SpriteList()

        self.textnoemie = arcade.Text("METS OUTSANDING STP",
                                      x=400, y=400, color=arcade.color.BLACK,
                                      font_size=20, anchor_x="center")
        self.easter_egg = False

        self.moves = []
        with open("output.txt", "r") as f:
            file = f.read()
        lines = file.split("\n")
        for li in lines:
            if li.startswith("D"):
                self.moves.append(li)

        self.score_text = arcade.Text(text="Tour: 0", x=20, y=750,
                                      color=arcade.color.BLACK, font_size=15)

    def setup(self):
        self.zone_lst = arcade.SpriteList()

        self.texts_to_draw = []
        self.draw_connections = []
        self.draw_max_drones = []

        self.distance_zones = 150

        self.drone_lst = arcade.SpriteList()
        self.drone_sprites = {}
        start_x, start_y = self.zones[0].get("Coordinates")

        for zone in self.zones:
            zone["drone_on_zone"] = 0
            x, y = zone.get("Coordinates")
            name = zone.get("Name")
            max_d = zone.get("Max_drones")
            find_color = zone.get("Color")
            color_upper = find_color.upper()
            color = getattr(arcade.color, color_upper, arcade.color.WHITE)
            zone_sprite = arcade.SpriteCircle(ZONES, color)
            zone_sprite.center_x = x * self.distance_zones
            zone_sprite.center_y = y * self.distance_zones
            self.zone_lst.append(zone_sprite)

            text = arcade.Text(
                text=name,
                x=x*self.distance_zones,
                y=y*self.distance_zones-40,
                color=color,
                font_size=12,
                anchor_x="center"
                )
            self.texts_to_draw.append(text)

            max_drones = arcade.Text(
                text=f"0/{max_d}",
                x=x*self.distance_zones+20,
                y=y*self.distance_zones+20,
                color=color,
                font_size=12
                )
            self.draw_max_drones.append(max_drones)

        for connection in self.connections:
            for zone in self.zones:
                if connection.get("Actual_Zone") == zone.get("Name"):
                    ax, ay = zone.get("Coordinates")
                elif connection.get("Zone_to_move_on") == zone.get("Name"):
                    bx, by = zone.get("Coordinates")
            self.draw_connections.append((ax*self.distance_zones,
                                          ay*self.distance_zones,
                                          bx*self.distance_zones,
                                          by*self.distance_zones))

        for drone in self.drones:
            for k, v in drone.items():
                if k.startswith("Drone"):
                    drone_id = v
            drone_sprite = arcade.SpriteCircle(DRONES, arcade.color.BLACK)
            drone_sprite.center_x = start_x * self.distance_zones
            drone_sprite.center_y = start_y * self.distance_zones
            self.drone_lst.append(drone_sprite)
            self.drone_sprites[drone_id] = drone_sprite

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == arcade.MOUSE_BUTTON_LEFT:
            curr_x, curr_y = self.camera.position
            new_x = curr_x - dx
            new_y = curr_y - dy
            self.camera.position = (new_x, new_y)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        zoom_speed = 0.1
        if scroll_y > 0:
            self.camera.zoom += zoom_speed
        elif scroll_y < 0:
            self.camera.zoom = max(0.1, self.camera.zoom - zoom_speed)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()
        if symbol == arcade.key.SPACE:
            self.easter_egg = not self.easter_egg

    def on_draw(self):
        self.clear()
        self.camera.use()
        for co in self.draw_connections:
            arcade.draw_line(co[0], co[1], co[2], co[3], arcade.color.GRAY, 2)
        self.zone_lst.draw()
        for text in self.texts_to_draw:
            text.draw()
        for max_d in self.draw_max_drones:
            max_d.draw()
        self.drone_lst.draw()

        self.gui_camera.use()
        self.score_text.draw()
        if self.easter_egg:
            self.textnoemie.draw()

    def move_drone(self):
        moves_for_this_turn = self.moves[self.turn]
        individual_move = moves_for_this_turn.split(" ")
        for move in individual_move:
            split_move = move.split("-")
            if len(split_move) == 3:
                drone_id = split_move[0]
                target_name = split_move[2]
                sprite = self.drone_sprites.get(drone_id)
                if sprite:
                    for zone in self.zones:
                        if zone.get("Name") == target_name:
                            dest_coords = zone.get("Coordinates")
                            dest_x = dest_coords[0] * self.distance_zones
                            dest_y = dest_coords[1] * self.distance_zones
                            target_x = (sprite.center_x + dest_x) // 2
                            target_y = (sprite.center_y + dest_y) // 2
                            sprite.target_x = target_x
                            sprite.target_y = target_y
                            sprite.change_x = (target_x - sprite.center_x) / 60
                            sprite.change_y = (target_y - sprite.center_y) / 60
                            break
            elif len(split_move) == 2:
                drone_id = split_move[0]
                target_name = split_move[1]
                sprite = self.drone_sprites.get(drone_id)
                if sprite:
                    for zone in self.zones:
                        if zone.get("Name") == target_name:
                            dest_coords = zone.get("Coordinates")
                            dest_x = dest_coords[0] * self.distance_zones
                            dest_y = dest_coords[1] * self.distance_zones
                            sprite.target_x = dest_x
                            sprite.target_y = dest_y
                            sprite.change_x = (dest_x - sprite.center_x) / 60
                            sprite.change_y = (dest_y - sprite.center_y) / 60
                            break
        self.turn += 1
        self.pause_for(5 * self.delta_time)

    def pause_for(self, seconds):
        self.paused = True
        self.pause_timer = 0
        self.pause_duration = seconds

    def on_update(self, delta_time):
        self.drone_lst.update()

        for zone in self.zones:
            zone["drone_on_zone"] = 0

        for drone in self.drone_lst:
            for i, zone_sprite in enumerate(self.zone_lst):
                if arcade.check_for_collision(drone, zone_sprite):
                    self.zones[i]["drone_on_zone"] += 1

        for i, zone in enumerate(self.zones):
            max_d = zone.get("Max_drones")
            drone_on_zone = zone.get("drone_on_zone", 0)
            self.draw_max_drones[i].value = f"{drone_on_zone}/{max_d}"

        for sprite in self.drone_lst:
            if hasattr(sprite, 'target_x'):
                diff_x = sprite.center_x - sprite.target_x
                diff_y = sprite.center_y - sprite.target_y
                dist = (diff_x**2 + diff_y**2)**0.5
                if dist < 2:
                    sprite.change_x = 0
                    sprite.change_y = 0
                    sprite.center_x = sprite.target_x
                    sprite.center_y = sprite.target_y

        if self.paused:
            self.pause_timer += delta_time
            if self.pause_timer >= self.pause_duration:
                self.paused = False
            return

        if self.turn < len(self.moves):
            self.time_elapsed += delta_time

        if self.time_elapsed > 1.0:
            if self.turn < len(self.moves):
                self.move_drone()
                self.score_text.text = f"Tour: {self.turn}"
                self.time_elapsed = 0
