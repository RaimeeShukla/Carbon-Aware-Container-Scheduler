from carbon_scheduler.execution.docker_executor import DockerExecutor
from carbon_scheduler.workloads.models import Workload

def main() -> None:
    workload = Workload(
        name="docker-smoke-test",
        command=["python", "-c", "print('Docker workload executed successfully')",],
        cpu_cores=0.5,
        memory_mb=256,
    )

    executor = DockerExecutor()

    try:
        result = executor.execute(workload)

        print(f"Workload: {result.workload_name}")
        print(f"Status: {result.status}")
        print(f"Exit code: {result.exit_code}")
        print(f"Duration: {result.duration_seconds:.3f}s")
        print(f"Logs:\n{result.logs}")

        if result.error:
            print(f"Error: {result.error}")

        if result.status != "completed":
            raise RuntimeError("Docker smoke test failed.")

    finally:
        executor.close()

if __name__ == "__main__":
    main()