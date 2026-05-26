import sys

from src.parser.parser import Parser
from src.utils.graph_debug import debug_print_graph
from src.graph.pathfinder import Pathfinder
from src.utils.path_debug import debug_print_path
from src.simulation.drone import Drone
from src.simulation.simulation import Simulation


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
    
    pathfinder = Pathfinder(graph)
    drones = [
        Drone(
            drone_id=i + 1,
            current_zone=graph.start,
        )
        for i in range(drone_count)
        ]
    path = pathfinder.shortest_path(
        graph.start,
        graph.end,
    )
    simulation = Simulation(
        graph=graph,
        drones=drones,
        path=path,
        )
    simulation.run()
    debug_print_path(path)


if __name__ == "__main__":
    main()
