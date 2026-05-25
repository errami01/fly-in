import sys

from src.parser.parser import Parser
from src.utils.graph_debug import debug_print_graph


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.main <map_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    parser = Parser()

    try:
        drone_count, graph = parser.parse(file_path)

        print("\n=== PARSE SUCCESS ===")
        print(f"Drones: {drone_count}")

        debug_print_graph(graph)

    

    except Exception as error:
        print(f"ERROR: {error}")


if __name__ == "__main__":
    main()
