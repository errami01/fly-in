from dataclasses import dataclass


@dataclass(slots=True)
class PlannedMove:
    drone_id: int

    from_zone: str
    to_zone: str

    is_restricted: bool = False
    completes_transit: bool = False