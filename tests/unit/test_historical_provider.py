import pytest

from datetime import datetime, timezone
from pathlib import Path
from carbon_scheduler.carbon.history import HistoricalCarbonProvider

FIXTURE_PATH = (Path(__file__).resolve().parents[1] / "fixtures" / "carbon_history.csv")

def test_load_historical_dataset():
    provider = HistoricalCarbonProvider(FIXTURE_PATH)

    assert provider.observation_count() == 6
    assert provider.available_regions() == ["france", "germany", "india"]

def test_query_exact_observation():
    provider = HistoricalCarbonProvider(FIXTURE_PATH)
    observation = provider.get_current_intensity("france", datetime(2026, 10, 26, 10, 0, tzinfo=timezone.utc))

    assert observation.intensity_gco2_per_kwh == 85.0
    assert observation.source == "test_fixture"

def test_query_timestamp_with_different_timezone_offset():
    provider = HistoricalCarbonProvider(FIXTURE_PATH)
    observation = provider.get_current_intensity("france", datetime.fromisoformat("2026-10-26T15:30:00+05:30"))
    assert observation.intensity_gco2_per_kwh == 85.0

def test_unknown_region_is_rejected():
    provider = HistoricalCarbonProvider(FIXTURE_PATH)
    with pytest.raises(ValueError, match="Unsupported region"):
        provider.get_current_intensity("spain", datetime(2026, 10, 26, 10, 0, tzinfo=timezone.utc))

def test_missing_timestamp_is_rejected():
    provider = HistoricalCarbonProvider(FIXTURE_PATH)
    with pytest.raises(LookupError, match="No observation"):
        provider.get_current_intensity("india", datetime(2026, 10, 26, 12, 0, tzinfo=timezone.utc))

def test_historical_query_requires_timestamp():
    provider = HistoricalCarbonProvider(FIXTURE_PATH)
    with pytest.raises(ValueError, match="explicit timestamp"):
        provider.get_current_intensity("india")

def test_naive_query_timestamp_is_rejected():
    provider = HistoricalCarbonProvider(FIXTURE_PATH)
    with pytest.raises(ValueError, match="timezone-aware"):
        provider.get_current_intensity("india", datetime(2026, 10, 26, 10, 0))

def test_missing_dataset_is_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        HistoricalCarbonProvider(tmp_path / "missing.csv")

def test_duplicate_region_timestamp_is_rejected(tmp_path):
    duplicate_csv = tmp_path / "duplicate.csv"
    duplicate_csv.write_text(
        "region,timestamp,intensity_gco2_per_kwh,source\n"
        "india,2026-10-26T10:00:00Z,650,test\n"
        "india,2026-10-26T10:00:00+00:00,640,test\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Duplicate observation"):
        HistoricalCarbonProvider(duplicate_csv)