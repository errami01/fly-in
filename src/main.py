import sys

from src.parser.parser import Parser


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
        print(f"Start: {graph.start}")
        print(f"End: {graph.end}")

        print("\n=== NODES ===")

        for node in graph.nodes.values():
            print(
                f"{node.name} "
                f"({node.x}, {node.y}) "
                f"type={node.zone_type.value} "
                f"capacity={node.max_drones} "
                f"neighbors={list(node.neighbors)}"
            )

        print("\n=== EDGES ===")

        for edge in graph.edges.values():
            print(
                f"{edge.start} <-> {edge.end} "
                f"capacity={edge.max_link_capacity}"
            )

    except Exception as error:
        print(f"ERROR: {error}")


if __name__ == "__main__":
    main()
