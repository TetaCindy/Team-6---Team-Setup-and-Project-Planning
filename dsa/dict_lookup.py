"""
Dictionary Lookup Implementation
Time Complexity: O(1)
Author: Cindy Saro Teta
"""

import json
import time


class DictionaryLookup:
    def __init__(self, data_file='data/processed/transactions.json'):
        with open(data_file, 'r') as f:
            data = json.load(f)
            self.transactions = data.get('transactions', [])
        
        self.index = {}
        for transaction in self.transactions:
            self.index[transaction.get('id')] = transaction
    
    def find_by_id(self, target_id):
        return self.index.get(target_id)
    
    def benchmark(self, search_ids):
        start_time = time.time()
        found_count = 0
        
        for search_id in search_ids:
            result = self.find_by_id(search_id)
            if result:
                found_count += 1
        
        elapsed_time = (time.time() - start_time) * 1000
        
        return {
            'algorithm': 'Dictionary Lookup',
            'dataset_size': len(self.transactions),
            'index_size': len(self.index),
            'searches': len(search_ids),
            'found': found_count,
            'total_time_ms': elapsed_time,
            'avg_time_ms': elapsed_time / len(search_ids),
            'total_comparisons': len(search_ids),
            'avg_comparisons': 1.0
        }


if __name__ == '__main__':
    lookup = DictionaryLookup()
    
    print("\n" + "="*60)
    print("DICTIONARY LOOKUP TESTING")
    print("="*60)
    print(f"Dataset size: {len(lookup.transactions)}")
    print(f"Index size: {len(lookup.index)}")
    
    result = lookup.find_by_id(1)
    print(f"\nSearch for ID=1: {'Found' if result else 'Not found'}")
    print(f"Comparisons: 1 (O(1) lookup)")
    
    print("\n" + "-"*60)
    print("Benchmark: Searching for 20 IDs")
    print("-"*60)
    
    search_ids = list(range(1, 21))
    results = lookup.benchmark(search_ids)
    
    print(f"Total searches: {results['searches']}")
    print(f"Found: {results['found']}")
    print(f"Total time: {results['total_time_ms']:.4f} ms")
    print(f"Average time: {results['avg_time_ms']:.6f} ms")
    print(f"Average comparisons: {results['avg_comparisons']:.2f}")
    print("="*60 + "\n")