def debug_print_path(path: list[str]) -> None:
    print("\n=== SHORTEST PATH ===")

    if not path:
        print("No path found")
        return

    print(" -> ".join(path))