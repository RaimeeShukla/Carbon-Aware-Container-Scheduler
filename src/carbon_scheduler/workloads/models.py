from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import uuid4

@dataclass
class Workload:
    name: str
    command: list[str]
    workload_id: str = field(default_factory=lambda: str(uuid4()))
    cpu_cores: float = 1.0
    memory_mb: int = 512
    estimated_duration_seconds: int = 60
    submitted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    earliest_start_time: Optional[datetime] = None
    deadline: Optional[datetime] = None
    allowed_regions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Workload name cannot be empty")

        if not self.command:
            raise ValueError("Workload command cannot be empty")

        if any(not arg.strip() for arg in self.command):
            raise ValueError("Command arguments cannot be empty")

        if self.cpu_cores <= 0:
            raise ValueError("CPU cores must be greater than zero")

        if self.memory_mb <= 0:
            raise ValueError("Memory must be greater than zero")

        if self.estimated_duration_seconds <= 0:
            raise ValueError("Estimated duration must be greater than zero")

        self._validate_timezone(self.submitted_at, "submitted_at")

        if self.earliest_start_time is not None:
            self._validate_timezone(self.earliest_start_time,"earliest_start_time")

            if self.earliest_start_time < self.submitted_at:
                raise ValueError("Earliest start time cannot precede submission time")

        if self.deadline is not None:
            self._validate_timezone(self.deadline, "deadline")
            effective_start = (self.earliest_start_time if self.earliest_start_time is not None else self.submitted_at)
            minimum_completion_time = (effective_start+ timedelta(seconds=self.estimated_duration_seconds))

            if self.deadline < minimum_completion_time:
                raise ValueError("Deadline leaves insufficient time for execution")

        if any(not region.strip() for region in self.allowed_regions):
            raise ValueError("Allowed region names cannot be empty")

    @staticmethod
    def _validate_timezone(value: datetime, field_name: str) -> None:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(f"{field_name} must be timezone-aware")