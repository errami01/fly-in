from src.constants import ZoneType
from src.exceptions import ParsingError


def parse_metadata(raw: str) -> dict[str, str]:
    metadata: dict[str, str] = {}

    if not raw:
        return metadata
    raw = raw.strip("[]")
    parts = raw.split()

    for part in parts:
        if "=" not in part:
            raise ParsingError(
                f"Invalid metadata entry: {part}"
            )

        key, value = part.split("=", maxsplit=1)

        metadata[key] = value

    return metadata


def validate_zone_type(zone_type: str) -> ZoneType:
    try:
        return ZoneType(zone_type)

    except ValueError as exc:
        raise ParsingError(
            f"Invalid zone type: {zone_type}"
        ) from exc
