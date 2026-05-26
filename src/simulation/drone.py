from dataclasses import dataclass


@dataclass(slots=True)
class Drone:
    drone_id: int
    current_zone: str
    delivered: bool = False
    