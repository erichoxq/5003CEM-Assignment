import random
import threading
import time

# Generate 100 random numbers
def generate_random_numbers():
    return [random.randint(0, 10000) for _ in range(100)]

# Thread task
def thread_task(result_list, index):
    result_list[index] = generate_random_numbers()

# Run multithreading for 10 rounds
def run_multithreading():
    times = []
    for _ in range(10):
        results = [None, None, None]
        threads = []

        start = time.time_ns()
        for i in range(3):
            t = threading.Thread(target=thread_task, args=(results, i))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        end = time.time_ns()
        times.append(end - start)
    return times

# Run without multithreading for 10 rounds
def run_non_threading():
    times = []
    for _ in range(10):
        start = time.time_ns()
        _ = generate_random_numbers()
        _ = generate_random_numbers()
        _ = generate_random_numbers()
        end = time.time_ns()
        times.append(end - start)
    return times

# Format number with commas and +/- sign for differences
def format_diff(n):
    return f"{n:+,}"

def format_num(n):
    return f"{n:,}"

# Display final results
def display_results(mt_times, nt_times):
    print("\nRound-by-Round Performance Comparison:")
    print("+--------+--------------------------+-------------------------------+-------------------------+")
    print("| Round  | Multithreading Time (ns) | Non-Multithreading Time (ns)  | Difference (ns)         |")
    print("+--------+--------------------------+-------------------------------+-------------------------+")

    total_mt = 0
    total_nt = 0

    for i in range(10):
        diff = mt_times[i] - nt_times[i]
        total_mt += mt_times[i]
        total_nt += nt_times[i]
        print(f"| {i+1:<6} | {format_num(mt_times[i]):<24} | {format_num(nt_times[i]):<29} | {format_diff(diff):<23} |")

    print("+--------+--------------------------+-------------------------------+-------------------------+\n")

    avg_mt = total_mt / 10
    avg_nt = total_nt / 10
    avg_diff = avg_mt - avg_nt

    print("Summary of Results:")
    print("+--------------+----------------------------+-------------------------------+-------------------------+")
    print("|   Metric     | Multithreading (ns)        | Non-Multithreading (ns)       | Difference (ns)         |")
    print("+--------------+----------------------------+-------------------------------+-------------------------+")
    print(f"| Total Time   | {format_num(total_mt):<26} | {format_num(total_nt):<29} | {format_diff(total_mt - total_nt):<23} |")
    print(f"| Average Time | {format_num(int(avg_mt)):<26} | {format_num(int(avg_nt)):<29} | {format_diff(int(avg_diff)):<23} |")
    print("+--------------+----------------------------+-------------------------------+-------------------------+")

# Main
if __name__ == "__main__":
    mt_results = run_multithreading()
    nt_results = run_non_threading()
    display_results(mt_results, nt_results)
