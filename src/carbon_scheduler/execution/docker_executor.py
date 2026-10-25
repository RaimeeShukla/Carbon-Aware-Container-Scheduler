import docker

from dataclasses import dataclass
from time import perf_counter
from docker.errors import DockerException, ImageNotFound
from carbon_scheduler.workloads.models import Workload

@dataclass
class ExecutionResult:
    workload_id: str
    workload_name: str
    status: str
    exit_code: int | None
    duration_seconds: float
    logs: str
    error: str | None = None

class DockerExecutor:
    def __init__(self, image: str = "python:3.12-slim", client=None) -> None:
        self.image = image
        self.client = client or docker.from_env()

    def execute(self, workload: Workload) -> ExecutionResult:
        start = perf_counter()
        container = None

        try:
            container = self.client.containers.run(
                image=self.image,
                command=workload.command,
                detach=True,
                mem_limit=f"{workload.memory_mb}m",
                nano_cpus=int(workload.cpu_cores * 1_000_000_000),
                network_disabled=True,
                read_only=True,
                cap_drop=["ALL"],
                security_opt=["no-new-privileges"],
                pids_limit=128,
            )

            result = container.wait()
            exit_code = result["StatusCode"]
            logs = container.logs(stdout=True, stderr=True).decode("utf-8", errors="replace")
            duration = perf_counter() - start

            return ExecutionResult(
                workload_id=workload.workload_id,
                workload_name=workload.name,
                status="completed" if exit_code == 0 else "failed",
                exit_code=exit_code,
                duration_seconds=duration,
                logs=logs,
            )

        except DockerException as exc:
            return ExecutionResult(
                workload_id=workload.workload_id,
                workload_name=workload.name,
                status="failed",
                exit_code=None,
                duration_seconds=perf_counter() - start,
                logs="",
                error=str(exc),
            )

        finally:
            if container is not None:
                try:
                    container.remove(force=True)
                except DockerException:
                    pass

    def close(self) -> None:
        self.client.close()