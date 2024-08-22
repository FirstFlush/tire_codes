from dataclasses import dataclass, asdict
from tire_codes.enums import TireCodeFormat

@dataclass
class TireSpecs:
    FORMAT: TireCodeFormat
    SERVICE_TYPE: str | None
    WIDTH: int
    ASPECT_RATIO: int | None
    WHEEL_DIAMETER: int
    CONSTRUCTION: str | None
    OVERALL_DIAMETER: float | None
    LOAD_INDEX: int | None
    LOAD_INDEX_DUAL: int | None
    SPEED_RATING: str | None

    def to_dict(self) -> dict:
        """
        Returns the tire specifications as a dictionary.

        This method provides a dictionary representation of the specs, 
        which may be preferred over accessing them through a separate class.
        """
        return asdict(self)