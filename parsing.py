from pydantic import BaseModel, Field, model_validator
from typing import Any

class MapConfig(BaseModel):
    nb_drones: int = Field(ge=1)
    start_hub: str = Field(min_length=8)
    hubs: dict
    end_hub: str = Field(min_length=8)
    connection: str = Field(min_length=8)


    @model_validator(mode="after")
    def validate_start(self) -> MapConfig:
        validate(self.start_hub)
        for k, v in self.hubs.items():
            validate(v)
        validate(self.end_hub)
        return self


def validate(zone_value: str):
    new_value = zone_value.split(" ", 3)
    if len(new_value) != 4:
        raise ValueError("informations missing about start_hub")
    for c in new_value[0]:
        if not c.isdigit() and not c.isalpha():
            raise ValueError("start_hub must have a name")

    try:
        int(new_value[1])
        int(new_value[2])
        if int(new_value[1]) < 0 or int(new_value[2]) < 0:
            raise ValueError("coordinates must be positives")
    except ValueError as e:
        raise ValueError(e)

    if not new_value[3].startswith("[") or not new_value[3].endswith("]"):
        raise ValueError("metadata must be surrounded by brackets")
    multiple = False
    for c in new_value[3]:
        if c == " ":
            multiple = True
    metadata_type = ["color", "zone", "max_drones"]
    possible_colors = ["blue", "red", "green", "orange"]
    possible_zones = ["normal", "blocked", "priority", "restricted"]

    if multiple:
        datas = new_value[3].split(" ")
        for data in datas:
            if data.startswith("["):
                data = data.strip("[")
            if data.endswith("]"):
                data = data.rstrip("]")
            clear_data = data.split("=")
            if clear_data[0] not in metadata_type:
                raise ValueError(f"invalid metadata '{clear_data[0]}'")
            if clear_data[0] == "color":
                if clear_data[1] not in possible_colors:
                    raise ValueError(f"invalid color '{clear_data[1]}'")
            elif clear_data[0] == "zone":
                if clear_data[1] not in possible_zones:
                    raise ValueError(f"invalid zone '{clear_data[1]}'")
            elif clear_data[0] == "max_drones":
                try:
                    int(clear_data[1])
                except ValueError:
                    raise ValueError(f"invalid number of drones '{clear_data[1]}'")
    else:
        metadatas = new_value[3].strip("[")
        metadatas = metadatas.rstrip("]")
        data = metadatas.split("=")
        if data[0] not in metadata_type:
            raise ValueError(f"invalid metadata '{data[0]}'")
        if data[0] == "color":
            if data[1] not in possible_colors:
                raise ValueError(f"invalid color '{data[1]}'")
        if data[0] == "zone":
                if data[1] not in possible_zones:
                    raise ValueError(f"invalid zone '{data[1]}'")
        if data[0] == "max_drones":
            try:
                int(data[1])
            except ValueError:
                raise ValueError(f"invalid number of drones '{data[1]}'")


def change_hub(key: str, i: int) -> str:
    return f"{key}{i}"


class Maps:
    def __init__(self, file: str) -> None:
        self.config: dict[str, Any] = {}
        i = 0

        mandatory_keys = ["nb_drones", "start_hub", "hub", "end_hub",
                          "connection"]
        with open(file, "r") as f:
            map_content = f.read().split("\n")
        for line in map_content:
            if line.startswith("#"):
                continue
            if not line.strip():
                continue
            param = line.split(":", 1)
            if len(param) != 2:
                raise KeyError(f"line must be key: value, got '{line}'")
            key, value = param[0].strip(), param[1].strip()
            if key not in mandatory_keys:
                raise KeyError(f"invalid key '{key}'")
            if key == "hub":
                i += 1
                key = change_hub(key, i)
            self.config[key] = value

        missing = [k for k in mandatory_keys if k not in self.config]
        if ', '.join(missing).startswith("hub"):
            pass
        elif missing:
            raise KeyError(f" missing mandatory key(s): '{', '.join(missing)}'")

        hub_dict = {}
        for key in self.config.keys():
            if key.startswith("hub"):
                hub_dict[key] = self.config[key]

        validated = MapConfig(
            nb_drones=self.config["nb_drones"],
            start_hub=self.config["start_hub"],
            hubs=hub_dict,
            end_hub=self.config["end_hub"],
            connection=self.config["connection"]
        )
        print(validated)

