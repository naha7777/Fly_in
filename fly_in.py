from sources.parsing import Maps
import sys
from sources.manager import Manager
from sources.algo import EdmondsKarp


def main() -> None:
    """Entry point: parse arguments, run simulation and animation."""
    show_datas = False
    try:
        if len(sys.argv) != 2 and len(sys.argv) != 3:
            raise ValueError("invalid number of arguments")
        if len(sys.argv) == 3:
            if sys.argv[1] == "show_datas":
                show_datas = True
            else:
                raise ValueError("invalid arguments")
            if not sys.argv[2].endswith(".txt"):
                raise ValueError("file must be a .txt")
            map = Maps(sys.argv[2])
        if len(sys.argv) == 2:
            if not sys.argv[1].endswith(".txt"):
                raise ValueError("file must be a .txt")
            map = Maps(sys.argv[1])
        manager = Manager(map.config)
        manager.create_zones()
        manager.get_zo_infos()
        manager.create_connections()
        manager.get_co_infos()
        matrice, s, e = manager.create_matrice()
        matrice_F, max_mouv = manager.create_algo(EdmondsKarp(matrice, s, e))
        manager.extract_paths(matrice_F)
        manager.create_drones()
        manager.simulate(max_mouv, show_datas)
        manager.animate()

    except (ValueError, KeyboardInterrupt, KeyError, PermissionError,
            FileNotFoundError, Exception) as e:
        print(f"ERROR: {e}")
        # import traceback
        # traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
