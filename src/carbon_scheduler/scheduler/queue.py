from collections import deque
from carbon_scheduler.workloads.models import Workload

class WorkloadQueue:
    def __init__(self) -> None:
        self._workloads: deque[Workload] = deque()
        self._workload_ids: set[str] = set()

    def enqueue(self, workload: Workload) -> None:
        if workload.workload_id in self._workload_ids:
            raise ValueError(f"Workload {workload.workload_id} is already queued")

        self._workloads.append(workload)
        self._workload_ids.add(workload.workload_id)

    def peek(self) -> Workload | None:
        if not self._workloads:
            return None

        return self._workloads[0]

    def dequeue(self) -> Workload | None:
        if not self._workloads:
            return None

        workload = self._workloads.popleft()
        self._workload_ids.remove(workload.workload_id)

        return workload

    def __len__(self) -> int:
        return len(self._workloads)

    def is_empty(self) -> bool:
        return not self._workloads