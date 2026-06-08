from dataclasses import dataclass


@dataclass(slots=True)
class ReplayMove:
    drone_id: int
    destination: str


@dataclass(slots=True)
class ReplayTurn:
    turn_number: int
    moves: list[ReplayMove]
    edge_usage: dict[
        tuple[str, str],
        int
    ]

@dataclass(slots=True)
class ReplayData:
    start_zone: str
    drone_count: int
    turns: list[ReplayTurn]
