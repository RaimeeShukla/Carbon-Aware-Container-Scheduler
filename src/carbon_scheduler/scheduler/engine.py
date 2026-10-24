from datetime import datetime, timedelta, timezone

from carbon_scheduler.scheduler.queue import WorkloadQueue
from carbon_scheduler.workloads.models import Workload


class BaselineScheduler:
    def __init__(self) -> None:
        self._queue = WorkloadQueue()

    def submit(self, workload: Workload) -> None:
        self._queue.enqueue(workload)

    def schedule_next(self, now: datetime | None = None) -> Workload | None:
        if now is None:
            now = datetime.now(timezone.utc)

        self._validate_timestamp(now)
        workload = self._queue.peek()

        if workload is None:
            return None

        if workload.earliest_start_time is not None:
            if now < workload.earliest_start_time:
                return None

        if workload.deadline is not None:
            estimated_completion = now + timedelta(seconds=workload.estimated_duration_seconds)

            if estimated_completion > workload.deadline:
                self._queue.dequeue()
                return self.schedule_next(now)

        return self._queue.dequeue()

    def pending_count(self) -> int:
        return len(self._queue)

    @staticmethod
    def _validate_timestamp(now: datetime) -> None:
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("Scheduling timestamp must be timezone-aware")