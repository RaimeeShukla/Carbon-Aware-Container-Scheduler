import csv

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from carbon_scheduler.carbon.base import CarbonDataProvider
from carbon_scheduler.carbon.models import CarbonIntensity


class HistoricalCarbonProvider(CarbonDataProvider):
    REQUIRED_COLUMNS = {"region", "timestamp", "intensity_gco2_per_kwh", "source"}
    SUPPORTED_REGIONS = {"india", "france", "germany"}

    def __init__(self, csv_path: str | Path) -> None:
        self.csv_path = Path(csv_path)
        self._observations: dict[str, dict[datetime, CarbonIntensity]] = defaultdict(dict)
        self._load_csv()

    def _load_csv(self) -> None:
        if not self.csv_path.is_file():
            raise FileNotFoundError(f"Carbon dataset not found: {self.csv_path}")

        with self.csv_path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError("Carbon dataset is empty.")

            missing_columns = self.REQUIRED_COLUMNS - set(reader.fieldnames)

            if missing_columns:
                raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

            for line_number, row in enumerate(reader, start=2):
                try:
                    region = row["region"].strip().lower()

                    if region not in self.SUPPORTED_REGIONS:
                        raise ValueError(f"Unsupported region: {region}")

                    timestamp = datetime.fromisoformat(row["timestamp"].strip().replace("Z", "+00:00"))

                    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
                        raise ValueError("Timestamp must include a timezone.")

                    timestamp = timestamp.astimezone(timezone.utc)
                    intensity = float(row["intensity_gco2_per_kwh"])
                    observation = CarbonIntensity(region=region, intensity_gco2_per_kwh=intensity, timestamp=timestamp, source=row["source"].strip())

                    if timestamp in self._observations[region]:
                        raise ValueError("Duplicate observation for region and timestamp")

                    self._observations[region][timestamp] = observation

                except (ValueError, TypeError, KeyError) as exc:
                    raise ValueError(f"Invalid carbon dataset row {line_number}: {exc}") from exc

    def get_current_intensity(self, region: str, at: datetime | None = None) -> CarbonIntensity:
        normalized_region = region.strip().lower()

        if normalized_region not in self.SUPPORTED_REGIONS:
            raise ValueError(f"Unsupported region: {region}")

        if at is None:
            raise ValueError("Historical queries require an explicit timestamp")

        if at.tzinfo is None or at.utcoffset() is None:
            raise ValueError("Query timestamp must be timezone-aware")

        timestamp = at.astimezone(timezone.utc)

        try:
            return self._observations[normalized_region][timestamp]
        except KeyError as exc:
            raise LookupError(f"No observation for {normalized_region} at {timestamp.isoformat()}") from exc

    def available_regions(self) -> list[str]:
        return sorted(region for region, observations in self._observations.items() if observations)

    def observation_count(self) -> int:
        return sum(len(observations) for observations in self._observations.values())