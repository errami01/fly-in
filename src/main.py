import sys
import argparse
from src.parser.parser import Parser
# from src.utils.graph_debug import debug_print_graph
# from src.graph.pathfinder import Pathfinder
from src.graph.route_allocator import RouteAllocator
# from src.utils.path_debug import debug_print_path
from src.simulation.drone import Drone
from src.simulation.simulation import Simulation
from src.visualization.pygame_visualizer import PygameVisualizer
from src.visualization.replay import ReplayData
from typing import cast


def main() -> None:
    arg_parser = argparse.ArgumentParser(description="A simple CLI tool.")
    arg_parser.add_argument(
        "file_path",
        type=str, help="The mandatory path to the map file")
    arg_parser.add_argument(
        "-v", "--visual",
        action="store_true", help="Visualize simulation")
    try:
        args = arg_parser.parse_args()
    except Exception:
        print("Usage: python -m src.main <map_file>")
        sys.exit(1)
    parser = Parser()

    try:
        drone_count, graph = parser.parse(args.file_path)

        # print("\n=== PARSE SUCCESS ===")
        # print(f"Drones: {drone_count}")

        # debug_print_graph(graph)

    except Exception as error:
        print(f"ERROR: {error}")
        return

    try:
        # pathfinder = Pathfinder(graph)

        drones = [
            Drone(
                drone_id=i + 1,
                current_zone=cast(str, graph.start),
            )
            for i in range(drone_count)
            ]
        # path = pathfinder.shortest_path(
        #     graph.start,
        #     graph.end,
        # )
        allocator = RouteAllocator(graph)

        drone_paths = allocator.allocate(drone_count)
        simulation = Simulation(
            graph=graph,
            drones=drones,
            drone_paths=drone_paths,
            )

        simulation.run()
        if args.visual:
            replay_data = ReplayData(
                start_zone=cast(str, graph.start),
                drone_count=len(simulation.drones),
                turns=simulation.replay_turns,
            )
            visualizer = PygameVisualizer(graph, replay_data)
            visualizer.run()
    except Exception as e:
        print(e)
    # debug_print_path(path)


if __name__ == "__main__":
    main()
