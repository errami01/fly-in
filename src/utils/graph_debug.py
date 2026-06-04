from src.graph.graph import Graph


def debug_print_graph(graph: Graph) -> None:
    print("\n=== GRAPH SUMMARY ===")

    print(f"Start Hub: {graph.start}")
    print(f"End Hub: {graph.end}")

    print(
        f"Nodes: {len(graph.nodes)} | "
        f"Edges: {len(graph.edges)}"
    )

    print("\n=== NODES ===")

    for node in graph.nodes.values():
        neighbors = ", ".join(sorted(node.neighbors))

        print(
            f"[{node.name}] "
            f"pos=({node.x},{node.y}) "
            f"type={node.zone_type.value} "
            f"color={node.color} "
            f"capacity={node.max_drones} "
            f"neighbors=[{neighbors}]"
        )

    print("\n=== CONNECTIONS ===")

    for edge in graph.edges.values():
        print(
            f"{edge.start} <-> {edge.end} "
            f"(capacity={edge.max_link_capacity})"
        )
