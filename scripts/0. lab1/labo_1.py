import contextlib
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from functools import wraps


# Decorator for measuring function execution time.
def timit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start time of function execution.
        result = func(*args, **kwargs)  # Execute the function.
        end_time = time.time()  # End time of function execution.
        # Print the execution time of the function.
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds to execute.")
        return result

    return wrapper


# Function to simulate a delay.
def wait_one_second(x):
    time.sleep(x)  # Sleep for 1 second.


# Context manager for managing thread lifecycle.
@contextmanager
def thread_manager(*args, **kwargs):
    thread = threading.Thread(*args, **kwargs)  # Create a new thread.
    thread.start()  # Start the thread.
    try:
        yield thread  # Yield control to the thread.
    finally:
        thread.join()  # Wait for the thread to finish.


# Function to demonstrate multithreading without context manager.
@timit
def multithreading(range_ten: range, wait):
    threads = []  # List to keep track of threads.
    for _ in range_ten:
        thread = threading.Thread(target=wait_one_second, args=(wait,))  # Create a thread.
        thread.start()  # Start the thread.
        threads.append(thread)  # Add thread to the list.
    for thread in threads:
        thread.join()  # Wait for all threads to complete.


# Function to demonstrate multithreading with context manager.
@timit
def multithreading_with_context_manager(range_ten: range, wait):
    with contextlib.ExitStack() as stack:
        # Use context manager to handle threads.
        [stack.enter_context(thread_manager(target=wait_one_second, args=(wait,))) for _ in range_ten]


# Function to demonstrate multithreading with ThreadPoolExecutor.
@timit
def multithreading_with_pool(n, wait):
    with ThreadPoolExecutor(max_workers=n) as executor:
        # Submit tasks to the executor.
        futures = [executor.submit(wait_one_second, wait) for _ in range(n)]
        for future in futures:
            future.result()  # Wait for all futures to complete.


# Function to simulate single-threaded execution.
@timit
def singlethreading(range_ten: range, wait):
    for _ in range_ten:
        wait_one_second(wait)  # Execute function in a single thread.


def main():
    n = 10_000
    wait = 1 / n
    range_ten = range(1, n + 1)  # Define a range from 1 to 10.
    # Execute functions to compare execution times.
    singlethreading(range_ten, wait)
    multithreading(range_ten, wait)
    multithreading_with_context_manager(range_ten, wait)
    multithreading_with_pool(n, wait)


if __name__ == "__main__":
    main()  # Entry point of the program.
