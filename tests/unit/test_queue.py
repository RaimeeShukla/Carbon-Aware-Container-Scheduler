import pytest

from carbon_scheduler.scheduler.queue import WorkloadQueue
from carbon_scheduler.workloads.models import Workload

def make_workload(name: str) -> Workload:
    return Workload(name=name, command=["python", "-c", "print('hello')"],)

def test_enqueue_and_dequeue():
    queue = WorkloadQueue()
    workload = make_workload("job-a")
    queue.enqueue(workload)

    assert len(queue) == 1
    assert queue.dequeue() == workload
    assert queue.is_empty()

def test_queue_preserves_fifo_order():
    queue = WorkloadQueue()
    
    first = make_workload("job-a")
    second = make_workload("job-b")

    queue.enqueue(first)
    queue.enqueue(second)
    assert queue.dequeue() == first
    assert queue.dequeue() == second

def test_peek_does_not_remove_workload():
    queue = WorkloadQueue()
    workload = make_workload("job-a")
    queue.enqueue(workload)
    assert queue.peek() == workload
    assert len(queue) == 1

def test_dequeue_empty_queue_returns_none():
    queue = WorkloadQueue()
    assert queue.dequeue() is None

def test_duplicate_queued_workload_is_rejected():
    queue = WorkloadQueue()
    workload = make_workload("job-a")
    queue.enqueue(workload)

    with pytest.raises(ValueError, match="already queued"):
        queue.enqueue(workload)