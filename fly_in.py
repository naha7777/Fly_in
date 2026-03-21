from parsing import Maps
import sys
from rich import print
from sources.manager import Manager


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("invalid number of arguments")
        if not sys.argv[1].endswith(".txt"):
            raise ValueError("file must be a .txt")
        # print("[red]bonjour[/red]")
        map = Maps(sys.argv[1])
        manager = Manager(map.config)
        manager.create_zones()
        manager.create_connections()
        manager.get_co_infos()
        manager.get_zo_infos()
        manager.create_matrice()
    except (ValueError, KeyboardInterrupt, KeyError, PermissionError,
            FileNotFoundError) as e:
        print(f"ERROR: {e}")
        exit(1)
