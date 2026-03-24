from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Any


save_coordinates: list[tuple[str, str]] = []
check_path = []
zones_blocked = []

validate_names: dict[str, str] = {}


def _validate_connection(zone_value: str, line: int, tt_line: int,
                         new_value: list[str]) -> None:
    """Validate syntax and semantics of a connection entry."""
    possible_co = ["max_link_capacity"]
    if "-" not in zone_value:
        raise ValueError(f"line {line}: invalid connection '{zone_value}' "
                         "'-' is missing between zones")
    if " " in zone_value:
        if "[" not in zone_value or "]" not in zone_value:
            raise ValueError(f"line {line}: metadata need to be surrounded"
                             " by brackets")
        separate_metadata = zone_value.split(" ")
        if len(separate_metadata) > 2:
            raise ValueError(f"line {line}: put only one metadata for"
                             " connection")
        clear_metadata = separate_metadata[1].rstrip("]").strip("[")
        if "=" not in clear_metadata:
            raise ValueError(f"line {line}: '=' missing in "
                             f"'{clear_metadata}'")
        separate_value = clear_metadata.split("=")
        if not separate_value[1] or not separate_value[1].isdigit()\
           or int(separate_value[1]) < 0:
            raise ValueError(f"line {line}: '{separate_value[1]}' is "
                             "incorrect, value must be a positive integer")
        if separate_value[0] not in possible_co:
            raise ValueError(f"line {line}: metadata '{separate_value[0]}'"
                             " incorrect")
    if zone_value.count("-") != 1:
        raise ValueError(f"line {line}: invalid connection '{zone_value}'"
                         "connection is only between two zones")
    disconnected = new_value[0].split("-")
    if disconnected[0] not in validate_names.values()\
       or disconnected[1] not in validate_names.values():
        raise ValueError(f"line {line}: connection impossible between"
                         f" unexistant zones '{new_value[0]}'")
    if disconnected[0] == disconnected[1]:
        raise ValueError(f"line {line}: can't create a connection between"
                         f" '{disconnected[0]}' and '{disconnected[1]}'")
    parts_path = (disconnected[0], disconnected[1])
    check_path.append(parts_path)

    if validate_names["end_hub"] in zones_blocked\
       or validate_names["start_hub"] in zones_blocked:
        raise ValueError(f"line {line}: connection impossible because "
                         "start and end can't be blocked zones")

    if line == tt_line:
        _check_path(line)


def _check_path(line: int) -> None:
    """
    Check that a path exists from start_hub to end_hub without blocked zones.
    """
    start_connected = False
    end_connected = False
    sort_check_path = []
    is_there_a_path = False
    find_a_path = []

    for i, v in enumerate(check_path):
        if i == 0 and validate_names["start_hub"] not in v:
            raise ValueError(f"line {line}: the first connection must contain "
                             "the start's zone")
        if validate_names["start_hub"] in v:
            if v[0] not in zones_blocked and v[0] not in find_a_path\
               and v[0] not in zones_blocked:
                find_a_path.append(v[0])
            if v[1] not in zones_blocked and v[1] not in find_a_path\
               and v[1] not in zones_blocked:
                find_a_path.append(v[1])
        if v[0] in find_a_path and v[0] not in zones_blocked:
            if v[1] == validate_names["end_hub"]:
                end_connected = True
                is_there_a_path = True
            else:
                find_a_path.append(v[1])
        elif v[1] in find_a_path and v[1] not in zones_blocked:
            if v[0] == validate_names["end_hub"]:
                end_connected = True
                is_there_a_path = True
            else:
                find_a_path.append(v[0])
        new_v = tuple(sorted(v))
        sort_check_path.append(new_v)
        if validate_names["start_hub"] in v:
            if validate_names["start_hub"] == v[0]:
                if len(find_a_path) == 0:
                    find_a_path.append(v[1])
                if v[1] not in zones_blocked:
                    start_connected = True
            elif validate_names["start_hub"] == v[1]:
                if len(find_a_path) == 0:
                    find_a_path.append(v[0])
                if v[0] not in zones_blocked:
                    start_connected = True
        if validate_names["end_hub"] in v:
            if v[0] not in zones_blocked:
                end_connected = True

    if not start_connected:
        raise ValueError(f"line {line}: missing connection with"
                         f" {validate_names['start_hub']}")
    if not end_connected:
        raise ValueError(f"line {line}: missing connection"
                         " with end_hub")
    if len(sort_check_path) != len(set(sort_check_path)):
        raise ValueError(f"line {line}: duplicate connections"
                         f" '{validate_names['connections']}'")
    if not is_there_a_path:
        raise ValueError(f"line {line}: start and end are never"
                         " connected")


def _validate_hub_metadata_multiple(new_value: list[str], line: int,
                                    metadata_type: list[str],
                                    possible_colors: list[str],
                                    possible_zones: list[str]) -> None:
    """Validate multiple space-separated metadata pairs inside brackets."""
    count_zone = 0
    count_color = 0
    count_max = 0
    datas = new_value[3].split(" ")
    if len(datas) > 3:
        raise ValueError(f"line {line}: there is only 3 metadatas possible"
                         f", not {len(datas)}")
    for data in datas:
        if data.startswith("["):
            data = data.strip("[")
        if data.endswith("]"):
            data = data.rstrip("]")
        c_data = data.split("=")
        if c_data[0] not in metadata_type:
            raise ValueError(f"line {line}: invalid metadata"
                             f" '{c_data[0]}'")
        if c_data[0] == "color":
            count_color += 1
            if c_data[1] not in possible_colors:
                raise ValueError(f"line {line}: invalid color"
                                 f" '{c_data[1]}'")
        elif c_data[0] == "zone":
            count_zone += 1
            if c_data[1] not in possible_zones:
                raise ValueError(f"line {line}: invalid zone"
                                 f" '{c_data[1]}'")
            if c_data[1] == "blocked":
                zones_blocked.append(new_value[0])
        elif c_data[0] == "max_drones":
            count_max += 1
            try:
                int(c_data[1])
                if int(c_data[1]) < 0:
                    raise ValueError(f"line {line}: max_drones can't be "
                                     f"negative '{c_data[1]}'")
            except ValueError:
                raise ValueError(f"line {line}: invalid number of drones"
                                 f" '{c_data[1]}'")
        if count_color > 1 or count_max > 1 or count_zone > 1:
            raise ValueError(f"line {line}: you can't put the same"
                             " metadata two times")


def _validate_hub_metadata_single(new_value: list[str], line: int,
                                  metadata_type: list[str],
                                  possible_colors: list[str],
                                  possible_zones: list[str]) -> None:
    """Validate a single metadata pair inside brackets."""
    metadatas = new_value[3].strip("[")
    metadatas = metadatas.rstrip("]")
    data = metadatas.split("=")
    if data[0] not in metadata_type:
        raise ValueError(f"line {line}: invalid metadata '{data[0]}'")
    if data[0] == "color":
        if data[1] not in possible_colors:
            raise ValueError(f"line {line}: invalid color '{data[1]}'")
    if data[0] == "zone":
        if data[1] not in possible_zones:
            raise ValueError(f"line {line}: invalid zone '{data[1]}'")
        if data[1] == "blocked":
            zones_blocked.append(new_value[0])
    if data[0] == "max_drones":
        try:
            int(data[1])
        except ValueError:
            raise ValueError(f"line {line}: invalid number of drones"
                             f" '{data[1]}'")


def _validate_hub(line: int, new_value: list[str]) -> None:
    """Validate a hub entry: name, coordinates, and optional metadata."""
    if len(new_value) != 4 and len(new_value) != 3:
        raise ValueError(f"line {line}: informations incorrect {new_value}")
    for c in new_value[0]:
        if c == " " or c == "-":
            raise ValueError(f"line {line}: '{new_value[0]}' is not a name")

    try:
        int(new_value[1])
        int(new_value[2])
    except ValueError:
        raise ValueError(f"line {line}: coordinates must be integers")

    coordinates = (new_value[1], new_value[2])
    if len(save_coordinates) > 0:
        if coordinates == save_coordinates[0]:
            raise ValueError(f"line {line}: hubs can't have the same"
                             " coordinates than start's coordinates")
    save_coordinates.append(coordinates)

    if len(new_value) == 3:
        return

    if not new_value[3].startswith("[") or not new_value[3].endswith("]"):
        raise ValueError(f"line {line}: metadata must be surrounded"
                         " by brackets")

    multiple = any(c == " " for c in new_value[3])
    metadata_type = ["color", "zone", "max_drones"]
    possible_colors = ["blue", "red", "green", "orange", "yellow", "cyan",
                       "pink", "purple", "brown", "lime", "magenta", "gold",
                       "black", "maroon", "darkred", "violet", "crimson",
                       "rainbow"]
    possible_zones = ["normal", "blocked", "priority", "restricted"]

    if multiple:
        _validate_hub_metadata_multiple(new_value, line, metadata_type,
                                        possible_colors, possible_zones)
    else:
        _validate_hub_metadata_single(new_value, line, metadata_type,
                                      possible_colors, possible_zones)


def validate(type: str, zone_value: str, line: int, tt_line: int) -> None:
    """Dispatch validation for a map entry (hub or connection)."""
    new_value = zone_value.split(" ", 3)

    validate_names[type] = new_value[0]
    if len(validate_names.values()) != len(set(validate_names.values())):
        raise ValueError(f"line {line}: duplicate hub names '{new_value[0]}'")

    if type == "connections":
        _validate_connection(zone_value, line, tt_line, new_value)
        return

    _validate_hub(line, new_value)


class MapConfig(BaseModel):
    """Pydantic model for a fully-parsed map configuration."""

    nb_drones: int = Field(ge=1)
    drones_line: int = Field(ge=1)
    start_hub: str = Field(min_length=1)
    start_line: int = Field(ge=1)
    hubs: dict[str, Any]
    hub_lines: list[int]
    end_hub: str = Field(min_length=1)
    end_line: int = Field(ge=1)
    connections: dict[str, Any]
    co_lines: list[int]
    tt_line: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_hubs(self) -> 'MapConfig':
        """Run semantic validation on all hubs and connections in order."""
        validate("start_hub", self.start_hub, self.start_line, self.tt_line)
        i = 0
        for k, v in self.hubs.items():
            if i < len(self.hub_lines):
                if i == 0:
                    hub = "hub"
                else:
                    hub = f"hub{i}"
                validate(hub, v, self.hub_lines[i], self.tt_line)
                i += 1
        validate("end_hub", self.end_hub, self.end_line, self.tt_line)
        i = 0
        for k, v in self.connections.items():
            if i < len(self.connections.items()):
                validate("connections", v, self.co_lines[i], self.tt_line)
                i += 1
        return self


def change_hub_or_connection(key: str, i: int) -> str:
    """Return ``key`` for i=0, or ``key<i>`` for subsequent occurrences."""
    if i == 0:
        return f"{key}"
    return f"{key}{i}"


class Maps:
    """Parse and validate a drone-map configuration file."""

    def __init__(self, file: str) -> None:
        """Parse and validate the map at *file*."""
        self.file = file
        self.config: dict[str, Any] = {}
        self.config = self.validate_config(file)

    def _init_counters(self) -> None:
        """Reset all per-file parsing counters."""
        self.i = 0
        self.j = 0
        self.first_key: list[str] = []
        self.start_count = -1
        self.end_count = -1
        self.line_count = 0
        self.mandatory_keys = ["nb_drones", "start_hub", "hub", "end_hub",
                               "connection"]

    def _read_file(self, file: str) -> list[str]:
        """Read the map file and return its lines."""
        with open(file, "r") as f:
            return f.read().split("\n")

    def _parse_line(self, line: str, hub_lines: list[int],
                    co_lines: list[int]) -> tuple[int | None, int | None,
                                                  int | None, int | None]:
        """Parse one line, update ``self.config``, and return line numbers."""
        drones_line = start_line = end_line = None

        if line.startswith("#") or not line.strip():
            return drones_line, start_line, end_line, None

        if line.count("]") > 1:
            raise ValueError(f"line {self.line_count}: metadatas can't be in"
                             " different brackets, please put it in the same"
                             " brackets with a space between each")

        if "#" in line:
            cut = line.split("#")
            line = cut[0]

        if line.startswith("start_hub"):
            self.start_count += 1
        if line.startswith("end_hub"):
            self.end_count += 1
        if self.start_count > 0 or self.end_count > 0:
            double_key = line.split(":")
            raise KeyError(f"line {self.line_count}: can't put duplicates"
                           f" keys: {double_key[0]}")

        if len(self.first_key) == 0:
            self.first_key.append(line)
        if line.startswith("nb_drones") and line not in self.first_key:
            raise KeyError(f"line {self.line_count}: nb_drones must be the"
                           " first key used")

        param = line.split(":", 1)
        if len(param) != 2:
            raise KeyError(f"line {self.line_count}: line must be key: "
                           f"value, got '{line}'")
        key, value = param[0].strip(), param[1].strip()
        if key not in self.mandatory_keys:
            raise KeyError(f"line {self.line_count}: invalid key '{key}'")

        if key == "hub":
            key = change_hub_or_connection(key, self.i)
            self.i += 1
        if key == "connection":
            key = change_hub_or_connection(key, self.j)
            self.j += 1
        self.config[key] = value

        if line.startswith("nb_drones"):
            drones_line = self.line_count
        elif line.startswith("start_hub"):
            start_line = self.line_count
        elif line.startswith("hub"):
            hub_lines.append(self.line_count)
        elif line.startswith("end_hub"):
            end_line = self.line_count
        elif line.startswith("connection"):
            co_lines.append(self.line_count)

        return drones_line, start_line, end_line, self.line_count

    def _build_sub_dicts(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Extract hub and connection sub-dicts from ``self.config``."""
        hub_dict = {k: v for k, v in self.config.items()
                    if k.startswith("hub")}
        co_dict = {k: v for k, v in self.config.items()
                   if k.startswith("connection")}
        return hub_dict, co_dict

    def _run_pydantic_validation(self, hub_dict: dict[str, Any],
                                 co_dict: dict[str, Any], drones_line: int,
                                 start_line: int, end_line: int,
                                 hub_lines: list[int], co_lines: list[int],
                                 tt_line: int) -> MapConfig:
        """
        Instantiate MapConfig and re-raise ValidationError with line info.
        """
        try:
            validated = MapConfig(
                nb_drones=self.config["nb_drones"],
                drones_line=drones_line,
                start_hub=self.config["start_hub"],
                start_line=start_line,
                hubs=hub_dict,
                hub_lines=hub_lines,
                end_hub=self.config["end_hub"],
                end_line=end_line,
                connections=co_dict,
                co_lines=co_lines,
                tt_line=tt_line
            )
        except ValidationError as e:
            for error in e.errors():
                if error.get("ctx") and error["ctx"].get("error"):
                    raise ValueError(str(error["ctx"]["error"]))
                field = error["loc"][0] if error["loc"] else "unknown"
                if field == "nb_drones":
                    error_line = drones_line
                elif field == "start_hub":
                    error_line = start_line
                elif field == "end_hub":
                    error_line = end_line
                msg = (error.get("msg") or "").replace("Value error, ", "")
                new_msg = msg.replace("Input", str(field))
                raise ValueError(f"line {error_line}: {new_msg}")
        return validated

    def validate_config(self, file: str) -> dict[str, Any]:
        """Parse the map file and return the validated configuration dict."""
        self._init_counters()
        map_content = self._read_file(file)

        hub_lines: list[int] = []
        co_lines: list[int] = []
        drones_line = start_line = end_line = tt_line = 0

        for line in map_content:
            self.line_count += 1
            dl, sl, el, tl = self._parse_line(line, hub_lines, co_lines)
            if dl is not None:
                drones_line = dl
            if sl is not None:
                start_line = sl
            if el is not None:
                end_line = el
            if tl is not None:
                tt_line = tl

        missing = [k for k in self.mandatory_keys if k not in self.config]
        if ', '.join(missing).startswith("hub"):
            pass
        elif missing:
            raise KeyError(f"line {self.line_count}: missing mandatory key(s):"
                           f" '{', '.join(missing)}'")

        hub_dict, co_dict = self._build_sub_dicts()

        validated = self._run_pydantic_validation(
            hub_dict, co_dict, drones_line, start_line, end_line,
            hub_lines, co_lines, tt_line
        )

        map_valid = {t: v for t, v in validated
                     if "line" not in t and "lines" not in t}
        return map_valid
