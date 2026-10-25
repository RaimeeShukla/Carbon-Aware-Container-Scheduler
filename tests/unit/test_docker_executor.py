from unittest.mock import MagicMock
from carbon_scheduler.execution.docker_executor import DockerExecutor
from carbon_scheduler.workloads.models import Workload
from docker.errors import DockerException

def make_workload() -> Workload:
    return Workload(name="test-job", command=["python", "-c", "print('hello')"], cpu_cores=0.5, memory_mb=256)

def test_successful_container_execution():
    client = MagicMock()
    container = MagicMock()

    container.wait.return_value = {"StatusCode": 0}
    container.logs.return_value = b"hello\n"

    client.containers.run.return_value = container
    executor = DockerExecutor(client=client)
    result = executor.execute(make_workload())

    assert result.status == "completed"
    assert result.exit_code == 0
    assert result.logs == "hello\n"
    assert result.duration_seconds >= 0

    client.containers.run.assert_called_once()
    container.remove.assert_called_once_with(force=True)


def test_failed_container_execution():
    client = MagicMock()
    container = MagicMock()

    container.wait.return_value = {"StatusCode": 1}
    container.logs.return_value = b"application error\n"

    client.containers.run.return_value = container
    executor = DockerExecutor(client=client)
    result = executor.execute(make_workload())

    assert result.status == "failed"
    assert result.exit_code == 1
    assert "application error" in result.logs
    container.remove.assert_called_once_with(force=True)


def test_docker_exception_returns_failed_result():
    client = MagicMock()
    client.containers.run.side_effect = DockerException("Docker unavailable")

    executor = DockerExecutor(client=client)
    result = executor.execute(make_workload())

    assert result.status == "failed"
    assert result.exit_code is None
    assert "Docker unavailable" in result.error