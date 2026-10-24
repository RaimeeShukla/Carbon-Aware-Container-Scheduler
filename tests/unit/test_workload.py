import pytest

from datetime import datetime, timedelta, timezone
from carbon_scheduler.workloads.models import Workload

def test_create_valid_workload():
    workload = Workload(name="cpu-benchmark", command=["python", "-c", "print('hello')"])

    assert workload.name == "cpu-benchmark"
    assert workload.cpu_cores == 1.0
    assert workload.memory_mb == 512
    assert workload.estimated_duration_seconds == 60
    assert workload.workload_id
    assert workload.submitted_at.tzinfo is not None

def test_workloads_receive_unique_ids():
    first = Workload(name="job-one", command=["python", "job.py"])
    second = Workload(name="job-two", command=["python", "job.py"],)
    assert first.workload_id != second.workload_id

@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("name", ""),
        ("command", []),
        ("cpu_cores", 0),
        ("memory_mb", 0),
        ("estimated_duration_seconds", 0),
    ],
)
def test_invalid_workload_values_are_rejected(field_name, value):
    arguments = {"name": "test-job", "command": ["python", "job.py"]}
    arguments[field_name] = value

    with pytest.raises(ValueError):
        Workload(**arguments)


def test_naive_submission_timestamp_is_rejected():
    with pytest.raises(ValueError, match="timezone-aware"):
        Workload(name="test-job", command=["python", "job.py"], submitted_at=datetime(2026, 10, 21, 10, 0))


def test_earliest_start_cannot_precede_submission():
    submitted_at = datetime(2026, 10, 21, 10, 0, tzinfo=timezone.utc)

    with pytest.raises(ValueError, match="cannot precede"):
        Workload(name="test-job", command=["python", "job.py"], submitted_at=submitted_at, earliest_start_time=submitted_at - timedelta(minutes=1))

def test_deadline_must_allow_enough_execution_time():
    submitted_at = datetime(2026, 10, 21, 10, 0, tzinfo=timezone.utc)

    with pytest.raises(ValueError, match="insufficient time"):
        Workload(name="test-job", command=["python", "job.py"], submitted_at=submitted_at, estimated_duration_seconds=600, deadline=submitted_at + timedelta(minutes=5))

def test_valid_deadline_and_allowed_regions():
    submitted_at = datetime(2026, 10, 21, 10, 0, tzinfo=timezone.utc)
    workload = Workload(name="batch-processing", command=["python", "process.py"], submitted_at=submitted_at, estimated_duration_seconds=600, earliest_start_time=submitted_at + timedelta(minutes=5), deadline=submitted_at + timedelta(minutes=30), allowed_regions=["france", "germany"])

    assert workload.earliest_start_time == submitted_at + timedelta(minutes=5)
    assert workload.deadline == submitted_at + timedelta(minutes=30)
    assert workload.allowed_regions == ["france", "germany"]