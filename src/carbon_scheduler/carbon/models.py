from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class CarbonIntensity:
    region: str
    intensity_gco2_per_kwh: float
    timestamp: datetime
    source: str

    def __post_init__(self) -> None:
        if not self.region.strip():
            raise ValueError("Region cannot be empty")

        if self.intensity_gco2_per_kwh < 0:
            raise ValueError("Carbon intensity cannot be negative")

        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise ValueError("Timestamp must be timezone-aware")

        if not self.source.strip():
            raise ValueError("Source cannot be empty")