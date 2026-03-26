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

        self.turn = 0

        self.drone_x_position = 0
        self.drone_x_pixels_per_second = 0

        self.zones = zones
        self.zone_lst = arcade.SpriteList()
        self.zone_name = arcade.Text(text="", x=0,y=0)

        self.camera = arcade.camera.Camera2D()
        self.camera.position = (0, 0)
        self.gui_camera = arcade.camera.Camera2D()

        self.texts_to_draw = []
        self.draw_connections = []

        self.connections = connections

        self.drones = drones
        self.drone_lst = arcade.SpriteList()

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
        self.zone_name = arcade.Text(text="", x=0,y=0)

        self.texts_to_draw = []
        self.draw_connections = []

        self.distance_beetween_zones = 150

        self.drone_lst = arcade.SpriteList()
        self.drone_sprites = {}
        start_x, start_y = self.zones[0].get("Coordinates")

        for zone in self.zones:
            x, y = zone.get("Coordinates")
            name = zone.get("Name")
            if zone.get("Type_Zone") == "blocked":
                circle_color = arcade.color.BLACK
            elif zone.get("Type_Zone") == "restricted":
                circle_color = arcade.color.DARK_RED
            elif zone.get("Type_Zone") == "priority":
                circle_color = arcade.color.GOLD
            elif zone.get("Type_Zone") == "normal":
                circle_color = arcade.color.GREEN
            zone_sprite = arcade.SpriteCircle(ZONES, circle_color)
            zone_sprite.center_x = x * self.distance_beetween_zones
            zone_sprite.center_y = y * self.distance_beetween_zones
            self.zone_lst.append(zone_sprite)

            text = arcade.Text(
                text=name,
                x=x*self.distance_beetween_zones,
                y=y*self.distance_beetween_zones-40,
                color= circle_color,
                font_size=12,
                anchor_x="center"
            )
            self.texts_to_draw.append(text)

        for connection in self.connections:
            for zone in self.zones:
                if connection.get("Actual_Zone") == zone.get("Name"):
                    ax, ay = zone.get("Coordinates")
                elif connection.get("Zone_to_move_on") == zone.get("Name"):
                    bx, by = zone.get("Coordinates")
            self.draw_connections.append((ax*self.distance_beetween_zones,
                                          ay*self.distance_beetween_zones,
                                          bx*self.distance_beetween_zones,
                                          by*self.distance_beetween_zones))

        for drone in self.drones:
            for k,v in drone.items():
                if k.startswith("Drone"):
                    drone_id = v
            drone_sprite = arcade.SpriteCircle(DRONES, arcade.color.BLACK)
            drone_sprite.center_x = start_x* self.distance_beetween_zones
            drone_sprite.center_y = start_y* self.distance_beetween_zones
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

    def on_draw(self):
        self.clear()
        self.camera.use()
        for co in self.draw_connections:
            arcade.draw_line(co[0], co[1], co[2], co[3], arcade.color.GRAY, 2)
        self.zone_lst.draw()
        for text in self.texts_to_draw:
            text.draw()
        self.drone_lst.draw()

        self.gui_camera.use()
        self.score_text.draw()

    def move_drone(self):
        if self.turn >= len(self.moves):
            for sprite in self.drone_sprites.values():
                sprite.change_x = 0
                sprite.change_y = 0
            return

        moves_for_this_turn = self.moves[self.turn]
        individual_move = moves_for_this_turn.split(" ")
        for move in individual_move:
            split_move = move.split("-")
            if len(split_move) == 3:
                for zone in self.zones:
                    if zone.get("Name") == split_move[2]:
                        dest_coords = zone.get("Coordinates")
                        dest_x = dest_coords[0]//2 * self.distance_beetween_zones
                        dest_y = dest_coords[1]//2 * self.distance_beetween_zones
                        sprite = self.drone_sprites[split_move[0]]
                        if not sprite:
                            continue
                        if sprite:
                            diff_x = dest_x - sprite.center_x // 2
                            diff_y = dest_y - sprite.center_y // 2
                            if abs(diff_x) < 1 and abs(diff_y) < 1:
                                sprite.change_x = 0
                                sprite.change_y = 0
                                sprite.center_x = dest_x // 2
                                sprite.center_y = dest_y // 2
                            else:
                                sprite.change_x = diff_x / 60
                                sprite.change_y = diff_y / 60
            elif len(split_move) == 2:
                for zone in self.zones:
                    if zone.get("Name") == split_move[1]:
                        dest_coords = zone.get("Coordinates")
                        dest_x = dest_coords[0] * self.distance_beetween_zones
                        dest_y = dest_coords[1] * self.distance_beetween_zones
                        sprite = self.drone_sprites[split_move[0]]
                        if sprite:
                            diff_x = dest_x - sprite.center_x
                            diff_y = dest_y - sprite.center_y
                            if abs(diff_x) < 1 and abs(diff_y) < 1:
                                sprite.change_x = 0
                                sprite.change_y = 0
                                sprite.center_x = dest_x
                                sprite.center_y = dest_y
                            else:
                                sprite.change_x = diff_x / 60
                                sprite.change_y = diff_y / 60
        self.turn += 1

    def on_update(self, delta_time):
        self.drone_lst.update()
        if self.turn < len(self.moves):
            self.time_elapsed += delta_time

        if self.time_elapsed > 1.0:
            if self.turn < len(self.moves):
                self.move_drone()
                self.score_text.text = f"Tour: {self.turn}"
                self.time_elapsed = 0

