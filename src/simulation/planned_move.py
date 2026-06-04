from dataclasses import dataclass
from typing import Tuple


@dataclass(slots=True)
class PlannedMove:
    drone_id: int

    from_zone: str
    to_zone: str

    is_restricted: bool = False
    completes_transit: bool = False

    def edge_key(self) -> Tuple[str, str]:
        z1, z2 = sorted([self.from_zone, self.to_zone])
        return (z1, z2)
