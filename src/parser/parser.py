import re
from src.constants import ZoneType
from src.exceptions import ParsingError
from src.graph.edge import ConnectionEdge
from src.graph.graph import Graph
from src.graph.node import ZoneNode
from src.parser.validator import parse_metadata, validate_zone_type


class Parser:
    NODE_PATTERN = re.compile(
        r"^(start_hub|end_hub|hub):"
        r"\s+([^\s]+)\s+(-?\d+)\s+(-?\d+)\s*(\[(.*)\])?$"
    )

    CONNECTION_PATTERN = re.compile(
        r"^connection:\s+([^\-]+)-([^\s]+)\s*(\[(.*)\])?$"
    )

    def _parse_connection(
            self,
            line: str,
            graph: Graph) -> None:
        match = self.CONNECTION_PATTERN.match(line)

        if match is None:
            raise ParsingError(
                "Invalid connection syntax"
            )

        start = match.group(1)
        end = match.group(2)
        metadata_raw = match.group(3)

        metadata = parse_metadata(metadata_raw or "")

        max_link_capacity = 1

        if "max_link_capacity" in metadata:
            value = metadata["max_link_capacity"]
            if not value.isdigit():
                raise ParsingError(
                    "max_link_capacity must be a positive integer"
                )

            max_link_capacity = int(value)

            if max_link_capacity <= 0:
                raise ParsingError(
                    "max_link_capacity must be greater than 0"
                )

        edge = ConnectionEdge(
            start=start,
            end=end,
            max_link_capacity=max_link_capacity,
        )

        graph.add_edge(edge)

    def _parse_drone_count(self, line: str) -> int:
        parts = line.split(":", maxsplit=1)

        if len(parts) != 2:
            raise ParsingError("Invalid nb_drones syntax")

        value = parts[1].strip()

        if not value.isdigit():
            raise ParsingError(
                "Drone count must be a positive integer"
            )

        drone_count = int(value)

        if drone_count <= 0:
            raise ParsingError(
                "Drone count must be greater than 0"
            )

        return drone_count

    def _parse_node(self, line: str, graph: Graph) -> None:
        match = self.NODE_PATTERN.match(line)

        if match is None:
            raise ParsingError("Invalid node syntax")

        node_kind = match.group(1)
        name = match.group(2)
        x = int(match.group(3))
        y = int(match.group(4))
        metadata_raw = match.group(5)

        metadata = parse_metadata(metadata_raw or "")

        zone_type = ZoneType.NORMAL
        color = "none"
        max_drones = 1

        if "zone" in metadata:
            zone_type = validate_zone_type(metadata["zone"])

        if "color" in metadata:
            color = metadata["color"]

        if "max_drones" in metadata:
            value = metadata["max_drones"]
            if not value.isdigit():
                raise ParsingError(
                    "max_drones must be a positive integer"
                )

            max_drones = int(value)

            if max_drones <= 0:
                raise ParsingError(
                    "max_drones must be greater than 0"
                )

        node = ZoneNode(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones,
        )

        graph.add_node(node)

        if node_kind == "start_hub":
            if graph.start is not None:
                raise ParsingError(
                    "Multiple start hubs detected"
                )

            graph.start = name

        elif node_kind == "end_hub":
            if graph.end is not None:
                raise ParsingError(
                    "Multiple end hubs detected"
                )

            graph.end = name

    def parse(self, file_path: str) -> tuple[int, Graph]:
        graph = Graph()

        drone_count: int | None = None

        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for index, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line:
                continue

            if line.startswith("#"):
                continue

            try:
                if line.startswith("nb_drones:"):
                    drone_count = self._parse_drone_count(line)
                    continue

                if line.startswith(("start_hub:", "end_hub:", "hub:")):
                    self._parse_node(line, graph)
                    continue
                if line.startswith("connection:"):
                    self._parse_connection(line, graph)
                    continue

                raise ParsingError("Unknown instruction")

            except Exception as exc:
                raise ParsingError(
                    f"Line {index}: {str(exc)}"
                ) from exc

        if drone_count is None:
            raise ParsingError("Missing drone count")

        if graph.start is None:
            raise ParsingError("Missing start hub")

        if graph.end is None:
            raise ParsingError("Missing end hub")

        return drone_count, graph
