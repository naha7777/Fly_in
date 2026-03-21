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
    except (ValueError, KeyboardInterrupt, KeyError, PermissionError,
            FileNotFoundError, Exception) as e:
        print(f"ERROR: {e}")
        exit(1)
