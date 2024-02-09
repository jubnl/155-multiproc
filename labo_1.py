import threading
import time
from functools import wraps


def timit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds to execute.")
        return result

    return wrapper


def wait_one_second():
    time.sleep(1)


@timit
def multithreading(range_ten: range):
    threads = []

    for _ in range_ten:
        thread = threading.Thread(target=wait_one_second)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


@timit
def singlethreading(range_ten: range):
    for _ in range_ten:
        wait_one_second()


def main():
    range_ten = range(1, 11)

    singlethreading(range_ten)
    multithreading(range_ten)


if __name__ == "__main__":
    main()
