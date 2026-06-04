from dataclasses import dataclass


@dataclass(slots=True)
class RouteAssignment:
    path: list[str]
    assigned_drones: int = 0
