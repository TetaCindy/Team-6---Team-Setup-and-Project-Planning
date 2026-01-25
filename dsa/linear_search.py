"""
Linear Search Implementation
Time Complexity: O(n)
"""

import json
import time


class LinearSearch:
    def __init__(self, data_file='data/processed/transactions.json'):
        with open(data_file, 'r') as f:
            data = json.load(f)
            self.transactions = data.get('transactions', [])
        
        self.comparisons = 0
    
    def find_by_id(self, target_id):
        self.comparisons = 0
        
        for transaction in self.transactions:
            self.comparisons += 1
            if transaction.get('id') == target_id:
                return transaction
        
        return None
    
    def benchmark(self, search_ids):
        start_time = time.time()
        total_comparisons = 0
        found_count = 0
        
        for search_id in search_ids:
            result = self.find_by_id(search_id)
            total_comparisons += self.comparisons
            if result:
                found_count += 1
        
        elapsed_time = (time.time() - start_time) * 1000
        
        return {
            'algorithm': 'Linear Search',
            'dataset_size': len(self.transactions),
            'searches': len(search_ids),
            'found': found_count,
            'total_time_ms': elapsed_time,
            'avg_time_ms': elapsed_time / len(search_ids),
            'total_comparisons': total_comparisons,
            'avg_comparisons': total_comparisons / len(search_ids)
        }


if __name__ == '__main__':
    searcher = LinearSearch()
    
    print("\n" + "="*60)
    print("LINEAR SEARCH TESTING")
    print("="*60)
    print(f"Dataset size: {len(searcher.transactions)}")
    
    result = searcher.find_by_id(1)
    print(f"\nSearch for ID=1: {'Found' if result else 'Not found'}")
    print(f"Comparisons: {searcher.comparisons}")
    
    print("\n" + "-"*60)
    print("Benchmark: Searching for 20 IDs")
    print("-"*60)
    
    search_ids = list(range(1, 21))
    results = searcher.benchmark(search_ids)
    
    print(f"Total searches: {results['searches']}")
    print(f"Found: {results['found']}")
    print(f"Total time: {results['total_time_ms']:.4f} ms")
    print(f"Average time: {results['avg_time_ms']:.6f} ms")
    print(f"Average comparisons: {results['avg_comparisons']:.2f}")
    print("="*60 + "\n")