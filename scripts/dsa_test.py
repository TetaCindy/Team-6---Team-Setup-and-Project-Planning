import time
import json
import os


def run_dsa_test():
    json_path = 'data/transactions.json'
    if not os.path.exists(json_path):
        print("Run the parser first to create transactions.json")
        return

    with open(json_path, 'r') as f:
        transactions_list = json.load(f)

    # Dictionary creation for O(1) lookup
    transactions_dict = {t['id']: t for t in transactions_list}

    # Test with the last ID to show worst-case linear performance
    target_id = transactions_list[-1]['id']

    # 1. Linear Search (O(n))
    start_linear = time.perf_counter()
    for t in transactions_list:
        if t['id'] == target_id:
            break
    end_linear = time.perf_counter()

    # 2. Dictionary Lookup (O(1))
    start_dict = time.perf_counter()
    _ = transactions_dict.get(target_id)
    end_dict = time.perf_counter()

    print("-" * 30)
    print("DSA PERFORMANCE RESULTS")
    print("-" * 30)
    print(f"Linear Search: {end_linear - start_linear:.8f}s")
    print(f"Dict Lookup:   {end_dict - start_dict:.8f}s")
    print("-" * 30)


if __name__ == "__main__":
    run_dsa_test()
