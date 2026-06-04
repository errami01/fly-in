from dataclasses import dataclass


@dataclass(slots=True)
class Drone:
    drone_id: int
    current_zone: str
    delivered: bool = False
    # Restricted-zone transit
    in_transit: bool = False
    transit_remaining: int = 0
    transit_destination: str | None = None
    transit_connection: tuple[str, str] | None = None
