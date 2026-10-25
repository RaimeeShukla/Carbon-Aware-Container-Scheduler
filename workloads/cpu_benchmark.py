import hashlib
import time

def main() -> None:
    start = time.perf_counter()
    data = b"carbon-aware-scheduler"

    for i in range(100_000):
        data = hashlib.sha256(data).digest()

    elapsed = time.perf_counter() - start

    print("CPU benchmark completed")
    print(f"Elapsed time: {elapsed:.4f} seconds")
    print(f"Final digest: {data.hex()}")

if __name__ == "__main__":
    main()