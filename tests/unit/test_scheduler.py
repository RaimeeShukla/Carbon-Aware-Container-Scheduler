import pytest

from datetime import datetime, timedelta, timezone
from carbon_scheduler.scheduler.engine import BaselineScheduler
from carbon_scheduler.workloads.models import Workload

NOW = datetime(2026, 10, 24, 10, 0, tzinfo=timezone.utc)

def make_workload(name: str, **kwargs,) -> Workload:
    return Workload(name=name, command=["python", "-c", "print('hello')"], submitted_at=NOW, **kwargs,)

def test_scheduler_selects_fifo_workload():
    scheduler = BaselineScheduler()
    first = make_workload("job-a")
    second = make_workload("job-b")

    scheduler.submit(first)
    scheduler.submit(second)

    assert scheduler.schedule_next(NOW) == first
    assert scheduler.schedule_next(NOW) == second
    assert scheduler.pending_count() == 0

def test_empty_scheduler_returns_none():
    scheduler = BaselineScheduler()
    assert scheduler.schedule_next(NOW) is None

def test_future_workload_is_not_selected_early():
    scheduler = BaselineScheduler()
    workload = make_workload("future-job", earliest_start_time=NOW + timedelta(minutes=10),)
    scheduler.submit(workload)

    assert scheduler.schedule_next(NOW) is None
    assert scheduler.pending_count() == 1

def test_workload_becomes_eligible_at_earliest_start():
    scheduler = BaselineScheduler()
    start_time = NOW + timedelta(minutes=10)
    workload = make_workload("future-job",earliest_start_time=start_time,)

    scheduler.submit(workload)
    assert scheduler.schedule_next(start_time) == workload

def test_workload_that_cannot_meet_deadline_is_skipped():
    scheduler = BaselineScheduler()
    impossible = make_workload("impossible-job", estimated_duration_seconds=600, deadline=NOW + timedelta(minutes=15))
    valid = make_workload("valid-job", estimated_duration_seconds=60, deadline=NOW + timedelta(minutes=20))

    scheduler.submit(impossible)
    scheduler.submit(valid)
    later_time = NOW + timedelta(minutes=10)

    assert scheduler.schedule_next(later_time) == valid
    assert scheduler.pending_count() == 0

def test_naive_scheduling_timestamp_is_rejected():
    scheduler = BaselineScheduler()

    with pytest.raises(ValueError, match="timezone-aware"):
        scheduler.schedule_next(datetime(2026, 10, 24, 10, 0))