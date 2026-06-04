from dataclasses import dataclass


@dataclass(slots=True)
class ConnectionEdge:
    start: str
    end: str
    max_link_capacity: int = 1

    def key(self) -> tuple[str, str]:
        return tuple(sorted((self.start, self.end)))
