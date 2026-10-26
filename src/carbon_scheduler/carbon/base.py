from abc import ABC, abstractmethod
from datetime import datetime
from carbon_scheduler.carbon.models import CarbonIntensity

class CarbonDataProvider(ABC):
    @abstractmethod
    def get_current_intensity(self, region: str, at: datetime | None = None) -> CarbonIntensity:
        raise NotImplementedError