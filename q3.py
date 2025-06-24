import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor
import statistics


def generate_random_numbers(count=100, min_val=0, max_val=10000):
    return [random.randint(min_val, max_val) for _ in range(count)]


def process_numbers_in_thread(thread_id, numbers):
    start_time = time.time_ns()

    processed_sum = sum(numbers)
    processed_avg = statistics.mean(numbers)
    processed_max = max(numbers)
    processed_min = min(numbers)

    for i in range(1000):
        temp = sum(numbers[j] * 2 for j in range(min(10, len(numbers))))
        # Simulate I/O latency so that threads can make progress concurrently
        time.sleep(0.001)  # 1 ms I/O wait

    end_time = time.time_ns()
    execution_time = end_time - start_time

    return {
        'thread_id': thread_id,
        'start_time': start_time,
        'end_time': end_time,
        'execution_time': execution_time,
        'sum': processed_sum,
        'average': processed_avg,
        'max': processed_max,
        'min': processed_min,
        'count': len(numbers)
    }


def run_multithreaded_experiment(rounds=10):
    results = []

    print("=" * 80)
    print("MULTITHREADED PROCESSING EXPERIMENT".center(80))
    print("=" * 80)

    for round_num in range(1, rounds + 1):
        print(f"\nRound {round_num}:")

        set1 = generate_random_numbers(100)
        set2 = generate_random_numbers(100)
        set3 = generate_random_numbers(100)

        overall_start = time.time_ns()

        with ThreadPoolExecutor(max_workers=3) as executor:
            future1 = executor.submit(process_numbers_in_thread, 'A', set1)
            future2 = executor.submit(process_numbers_in_thread, 'B', set2)
            future3 = executor.submit(process_numbers_in_thread, 'C', set3)

            result1 = future1.result()
            result2 = future2.result()
            result3 = future3.result()

        overall_end = time.time_ns()

        thread_start_times = [result1['start_time'], result2['start_time'], result3['start_time']]
        thread_end_times = [result1['end_time'], result2['end_time'], result3['end_time']]

        first_start = min(thread_start_times)
        last_end = max(thread_end_times)
        total_time = last_end - first_start

        round_result = {
            'round': round_num,
            'total_time_ns': total_time,
            'thread_results': [result1, result2, result3],
            'overall_start': overall_start,
            'overall_end': overall_end
        }

        results.append(round_result)

        print(f"  Thread A: {result1['execution_time']:,} ns")
        print(f"  Thread B: {result2['execution_time']:,} ns")
        print(f"  Thread C: {result3['execution_time']:,} ns")
        print(f"  Total Time: {total_time:,} ns")

    return results


def run_non_multithreaded_experiment(rounds=10):
    results = []

    print("\n" + "=" * 80)
    print("NON-MULTITHREADED PROCESSING EXPERIMENT".center(80))
    print("=" * 80)

    for round_num in range(1, rounds + 1):
        print(f"\nRound {round_num}:")

        set1 = generate_random_numbers(100)
        set2 = generate_random_numbers(100)
        set3 = generate_random_numbers(100)

        start_time = time.time_ns()

        result1 = process_numbers_in_thread('A', set1)
        result2 = process_numbers_in_thread('B', set2)
        result3 = process_numbers_in_thread('C', set3)

        end_time = time.time_ns()
        total_time = end_time - start_time

        round_result = {
            'round': round_num,
            'total_time_ns': total_time,
            'thread_results': [result1, result2, result3]
        }

        results.append(round_result)

        print(f"  Set A: {result1['execution_time']:,} ns")
        print(f"  Set B: {result2['execution_time']:,} ns")
        print(f"  Set C: {result3['execution_time']:,} ns")
        print(f"  Total Time: {total_time:,} ns")

    return results


def display_comparison_results(multithreaded_results, non_multithreaded_results):
    print("\n" + "=" * 100)
    print("PERFORMANCE COMPARISON RESULTS".center(100))
    print("=" * 100)

    print("\nRound-by-Round Performance Comparison:".center(100))

    # Improved table formatting with balanced columns
    col1_width = 7  # Round
    col2_width = 25  # Multithreading Time
    col3_width = 30  # Non-Multithreading Time
    col4_width = 17  # Difference

    # Create separator line
    separator = "+" + "-" * 9 + "+" + "-" * 27 + "+" + "-" * 32 + "+" + "-" * 19 + "+"

    print(separator)

    # Header row with centered text
    header = (f"| {'Round'.center(col1_width)} | "
              f"{'Multithreading Time (ns)'.center(col2_width)} | "
              f"{'Non-Multithreading Time (ns)'.center(col3_width)} | "
              f"{'Difference (ns)'.center(col4_width)} |")
    print(header)
    print(separator)

    differences = []
    for i in range(len(multithreaded_results)):
        mt_time = multithreaded_results[i]['total_time_ns']
        nmt_time = non_multithreaded_results[i]['total_time_ns']
        diff = mt_time - nmt_time
        differences.append(diff)

        # Format row with centered content
        row = (f"| {str(i + 1).center(col1_width)} | "
               f"{f'{mt_time:,}'.center(col2_width)} | "
               f"{f'{nmt_time:,}'.center(col3_width)} | "
               f"{f'{diff:+,}'.center(col4_width)} |")
        print(row)

    print(separator)

    mt_times = [r['total_time_ns'] for r in multithreaded_results]
    nmt_times = [r['total_time_ns'] for r in non_multithreaded_results]

    mt_total = sum(mt_times)
    nmt_total = sum(nmt_times)
    mt_avg = statistics.mean(mt_times)
    nmt_avg = statistics.mean(nmt_times)

    print("\nSummary of Results:".center(100))

    # Summary table formatting
    sum_col1_width = 15  # Metric
    sum_col2_width = 25  # Multithreading
    sum_col3_width = 25  # Non-Multithreading
    sum_col4_width = 17  # Difference

    sum_separator = ("+" + "-" * 17 + "+" + "-" * 27 +
                     "+" + "-" * 27 + "+" + "-" * 19 + "+")

    print(sum_separator)

    # Summary header
    sum_header = (f"| {'Metric'.center(sum_col1_width)} | "
                  f"{'Multithreading (ns)'.center(sum_col2_width)} | "
                  f"{'Non-Multithreading (ns)'.center(sum_col3_width)} | "
                  f"{'Difference (ns)'.center(sum_col4_width)} |")
    print(sum_header)
    print(sum_separator)

    # Total time row
    total_row = (f"| {'Total Time'.center(sum_col1_width)} | "
                 f"{f'{mt_total:,}'.center(sum_col2_width)} | "
                 f"{f'{nmt_total:,}'.center(sum_col3_width)} | "
                 f"{f'{mt_total - nmt_total:+,}'.center(sum_col4_width)} |")
    print(total_row)

    # Average time row
    avg_row = (f"| {'Average Time'.center(sum_col1_width)} | "
               f"{f'{mt_avg:,.1f}'.center(sum_col2_width)} | "
               f"{f'{nmt_avg:,.1f}'.center(sum_col3_width)} | "
               f"{f'{mt_avg - nmt_avg:+,.1f}'.center(sum_col4_width)} |")
    print(avg_row)
    print(sum_separator)

    return {
        'multithreaded_total': mt_total,
        'non_multithreaded_total': nmt_total,
        'multithreaded_average': mt_avg,
        'non_multithreaded_average': nmt_avg,
        'differences': differences
    }


def main():
    random.seed(42)

    mt_results = run_multithreaded_experiment(10)
    nmt_results = run_non_multithreaded_experiment(10)
    comparison = display_comparison_results(mt_results, nmt_results)


if __name__ == "__main__":
    main()