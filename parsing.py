from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Any


def validate(type: str, zone_value: str, line: int) -> None:
    new_value = zone_value.split(" ", 3)
    if not hasattr(validate, "names"):
        validate.names = []

    validate.names.append(new_value[0])
    if len(validate.names) != len(set(validate.names)):
        if "-" in new_value[0]:
            raise ValueError(f"line {line}: duplicate connections"
                             f" '{new_value[0]}'")
        raise ValueError(f"line {line}: duplicate hub names '{new_value[0]}'")

    if type == "connections":
        possible_co = ["max_link_capacity"]
        if "-" not in zone_value:
            raise ValueError(f"line {line}: invalid connection '{zone_value}' "
                             "'-' is missing between zones")
        if " " in zone_value:
            if "[" not in zone_value or "]" not in zone_value:
                raise ValueError(f"line {line}: metadata need to be surrounded"
                                 " by brackets")
            separate_metadata = zone_value.split(" ")
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
        disconnected = new_value[0].split("-")
        if disconnected[0] not in validate.names\
           or disconnected[1] not in validate.names:
            raise ValueError(f"line {line}: connection impossible between"
                             f" unexistant zones '{new_value[0]}'")
        if disconnected[0] == disconnected[1]:
            raise ValueError(f"line {line}: can't create a connection between"
                             f" '{disconnected[0]}' and '{disconnected[1]}'")
        return

    if len(new_value) != 4:
        raise ValueError(f"line {line}: informations incorrect {new_value}")
    for c in new_value[0]:
        if c == " " or c == "-":
            raise ValueError(f"line {line}: '{new_value[0]}' is not a name")

    try:
        int(new_value[1])
        int(new_value[2])
    except ValueError:
        raise ValueError(f"line {line}: coordinates must be integers")

    if not new_value[3].startswith("[") or not new_value[3].endswith("]"):
        raise ValueError(f"line {line}: metadata must be surrounded"
                         " by brackets")
    multiple = False
    for c in new_value[3]:
        if c == " ":
            multiple = True
    metadata_type = ["color", "zone", "max_drones", ""]
    possible_colors = ["blue", "red", "green", "orange", "yellow", "cyan"]
    possible_zones = ["normal", "blocked", "priority", "restricted"]

    if multiple:
        datas = new_value[3].split(" ")
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
                if c_data[1] not in possible_colors:
                    raise ValueError(f"line {line}: invalid color"
                                     f" '{c_data[1]}'")
            elif c_data[0] == "zone":
                if c_data[1] not in possible_zones:
                    raise ValueError(f"line {line}: invalid zone"
                                     f" '{c_data[1]}'")
            elif c_data[0] == "max_drones":
                try:
                    int(c_data[1])
                    if int(c_data[1]) < 0:
                        raise ValueError(f"line {line}: max_drones can't be "
                                         f"negative '{c_data[1]}'")
                except ValueError:
                    raise ValueError(f"line {line}: invalid number of drones"
                                     f" '{c_data[1]}'")
    else:
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
        if data[0] == "max_drones":
            try:
                int(data[1])
            except ValueError:
                raise ValueError(f"line {line}: invalid number of drones"
                                 f" '{data[1]}'")


class MapConfig(BaseModel):
    nb_drones: int = Field(ge=1)
    drones_line: int = Field(ge=1)
    start_hub: str = Field(min_length=8)
    start_line: int = Field(ge=1)
    hubs: dict
    hub_lines: list
    end_hub: str = Field(min_length=8)
    end_line: int = Field(ge=1)
    connections: dict
    co_lines: list

    @model_validator(mode="after")
    def validate_hubs(self) -> 'MapConfig':
        validate("start_hub", self.start_hub, self.start_line)
        i = 0
        for k, v in self.hubs.items():
            if i < len(self.hub_lines):
                validate("hub", v, self.hub_lines[i])
                i += 1
        validate("end_hub", self.end_hub, self.end_line)
        i = 0
        for k, v in self.connections.items():
            if i < len(self.connections.items()):
                validate("connections", v, self.co_lines[i])
                i += 1
        return self


def change_hub_or_connection(key: str, i: int) -> str:
    if i == 0:
        return f"{key}"
    return f"{key}{i}"


class Maps:
    def __init__(self, file: str) -> None:
        self.file = file
        self.config: dict[str, Any] = {}
        self.config = self.validate_config(file)

    def validate_config(self, file: str) -> dict:
        self.i = 0
        self.j = 0
        self.first_key = []
        self.start_count = -1
        self.end_count = -1
        self.line_count = 0
        self.mandatory_keys = ["nb_drones", "start_hub", "hub", "end_hub",
                               "connection"]
        with open(file, "r") as f:
            map_content = f.read().split("\n")
        hub_lines = []
        co_lines = []
        for line in map_content:
            self.line_count += 1
            if line.startswith("#"):
                continue
            if not line.strip():
                continue
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

        missing = [k for k in self.mandatory_keys if k not in self.config]
        if ', '.join(missing).startswith("hub"):
            pass
        elif missing:
            raise KeyError(f"line {self.line_count}: missing mandatory key(s):"
                           f" '{', '.join(missing)}'")

        hub_dict = {}
        for key in self.config.keys():
            if key.startswith("hub"):
                hub_dict[key] = self.config[key]
        co_dict = {}
        for key in self.config.keys():
            if key.startswith("connection"):
                co_dict[key] = self.config[key]

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
                co_lines=co_lines
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
                new_msg = msg.replace("Input", field)
                raise ValueError(f"line {error_line}: {new_msg}")
        map_valid = {}
        for t, v in validated:
            if "line" not in t and "lines" not in t:
                map_valid[t] = v
        return (map_valid)
