import math

from datetime import datetime, timezone
from carbon_scheduler.carbon.base import CarbonDataProvider
from carbon_scheduler.carbon.models import CarbonIntensity

class SyntheticCarbonProvider(CarbonDataProvider):
    BASE_INTENSITY = {"india": 650.0, "france": 80.0, "germany": 350.0,}
    AMPLITUDE = {"india": 100.0, "france": 25.0, "germany": 90.0,}

    def get_current_intensity(self, region: str, at: datetime | None = None) -> CarbonIntensity:
        normalized_region = region.strip().lower()

        if normalized_region not in self.BASE_INTENSITY:
            raise ValueError(f"Unsupported region: {region}")

        timestamp = at or datetime.now(timezone.utc)

        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("Timestamp must be timezone-aware")

        hour = timestamp.hour + timestamp.minute / 60.0
        base = self.BASE_INTENSITY[normalized_region]
        amplitude = self.AMPLITUDE[normalized_region]
        intensity = base + amplitude * math.sin(2 * math.pi * (hour - 6) / 24)

        return CarbonIntensity(region=normalized_region, intensity_gco2_per_kwh=round(max(0.0, intensity), 2), timestamp=timestamp, source="synthetic")