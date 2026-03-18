from parsing import MapConfig, Maps
import sys
import pydantic

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("invalid number of arguments")
        if not sys.argv[1].endswith(".txt"):
            raise ValueError("file must be a .txt")
        map = Maps(sys.argv[1])
    except pydantic.ValidationError as e:
        for error in e.errors():
            print(f"ERROR: {error['msg'].replace('Value error, ', '')}")
    except (ValueError, KeyboardInterrupt, KeyError, PermissionError,
            FileNotFoundError, Exception) as e:
       print(f"ERROR: {e}")
       exit(1)
