import pytest

from datetime import datetime, timezone
from carbon_scheduler.carbon.models import CarbonIntensity
from carbon_scheduler.carbon.synthetic_provider import SyntheticCarbonProvider

def test_carbon_intensity_accepts_valid_data():
    observation = CarbonIntensity(region="france", intensity_gco2_per_kwh=90.0, timestamp=datetime(2026, 10, 26, 12, 0, tzinfo=timezone.utc), source="test")
    assert observation.region == "france"
    assert observation.intensity_gco2_per_kwh == 90.0

def test_negative_carbon_intensity_is_rejected():
    with pytest.raises(ValueError, match="cannot be negative"):
        CarbonIntensity(region="france", intensity_gco2_per_kwh=-10.0, timestamp=datetime(2026, 10, 26, 12, 0, tzinfo=timezone.utc), source="test")

def test_naive_timestamp_is_rejected():
    with pytest.raises(ValueError, match="timezone-aware"):
        CarbonIntensity(region="france", intensity_gco2_per_kwh=90.0, timestamp=datetime(2026, 10, 26, 12, 0), source="test")

def test_synthetic_provider_supports_three_regions():
    provider = SyntheticCarbonProvider()
    timestamp = datetime(2026, 10, 26, 12, 0, tzinfo=timezone.utc)

    for region in ("india", "france", "germany"):
        observation = provider.get_current_intensity(region, timestamp)

        assert observation.region == region
        assert observation.intensity_gco2_per_kwh >= 0
        assert observation.source == "synthetic"
        assert observation.timestamp == timestamp

def test_synthetic_provider_is_deterministic():
    provider = SyntheticCarbonProvider()
    timestamp = datetime(2026, 10, 26, 12, 0, tzinfo=timezone.utc)
    first = provider.get_current_intensity("france", timestamp)
    second = provider.get_current_intensity("france", timestamp)

    assert first == second

def test_synthetic_provider_rejects_unknown_region():
    provider = SyntheticCarbonProvider()
    with pytest.raises(ValueError, match="Unsupported region"):
        provider.get_current_intensity("spain")

def test_synthetic_provider_rejects_naive_timestamp():
    provider = SyntheticCarbonProvider()
    with pytest.raises(ValueError, match="timezone-aware"):
        provider.get_current_intensity("india", datetime(2026, 10, 26, 12, 0))