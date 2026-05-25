from dataclasses import dataclass, field

from src.constants import ZoneType


@dataclass(slots=True)
class ZoneNode:
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str = "none"
    max_drones: int = 1
    neighbors: dict[str, "ConnectionEdge"] = field(default_factory=dict)

    def is_blocked(self) -> bool:
        return self.zone_type == ZoneType.BLOCKED

    def movement_cost(self) -> int:
        if self.zone_type == ZoneType.RESTRICTED:
            return 2

        return 1