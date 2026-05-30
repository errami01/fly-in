from dataclasses import dataclass


@dataclass(slots=True)
class PlannedMove:
    drone_id: int

    from_zone: str
    to_zone: str

    is_restricted: bool = False
    completes_transit: bool = False

    def edge_key(self) -> tuple[str, str]:
        return tuple(
            sorted(
                (
                    self.from_zone,
                    self.to_zone,
                )
            )
        )