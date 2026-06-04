def debug_print_path(path: list[str]) -> None:
    print("\n=== SHORTEST PATH ===")

    if not path:
        print("No path found")
        return

    print(" -> ".join(path))


def print_allocated_paths(paths: dict[int, list[str]]):
    print("\n=== ROUTE ASSIGNMENTS ===")

    for drone_id, path in paths.items():
        print(f"D{drone_id}: " + " -> ".join(path))
