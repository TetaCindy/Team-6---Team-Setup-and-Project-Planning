"""
Performance Comparison: Linear Search vs Dictionary Lookup
"""

from linear_search import LinearSearch
from dict_lookup import DictionaryLookup
import json


def run_comparison():
    print("\n" + "="*70)
    print("PERFORMANCE COMPARISON: Linear Search vs Dictionary Lookup")
    print("="*70)
    
    linear = LinearSearch()
    dictionary = DictionaryLookup()
    
    print(f"\nDataset Size: {len(linear.transactions)} transactions")
    
    scenarios = [
        ('Small (5 IDs)', list(range(1, 6))),
        ('Medium (10 IDs)', list(range(1, 11))),
        ('Large (20 IDs)', list(range(1, 21))),
    ]
    
    results_summary = []
    
    for name, search_ids in scenarios:
        print(f"\n{'-'*70}")
        print(f"Scenario: {name}")
        print(f"{'-'*70}")
        
        linear_results = linear.benchmark(search_ids)
        print(f"\nLinear Search:")
        print(f"  Time: {linear_results['total_time_ms']:.4f} ms")
        print(f"  Avg Time: {linear_results['avg_time_ms']:.6f} ms")
        print(f"  Avg Comparisons: {linear_results['avg_comparisons']:.2f}")
        
        dict_results = dictionary.benchmark(search_ids)
        print(f"\nDictionary Lookup:")
        print(f"  Time: {dict_results['total_time_ms']:.4f} ms")
        print(f"  Avg Time: {dict_results['avg_time_ms']:.6f} ms")
        print(f"  Avg Comparisons: {dict_results['avg_comparisons']:.2f}")
        
        speedup = linear_results['total_time_ms'] / dict_results['total_time_ms'] if dict_results['total_time_ms'] > 0 else 0
        print(f"\nDictionary is {speedup:.2f}x faster")
        
        results_summary.append({
            'scenario': name,
            'linear_time': linear_results['total_time_ms'],
            'dict_time': dict_results['total_time_ms'],
            'speedup': speedup
        })
    
    print("\n" + "="*70)
    print("SUMMARY & ANALYSIS")
    print("="*70)
    print("\nTime Complexity:")
    print("  Linear Search:     O(n) - checks each element")
    print("  Dictionary Lookup: O(1) - direct hash access")
    
    print("\nSpace Complexity:")
    print("  Linear Search:     O(1) - no extra space")
    print("  Dictionary Lookup: O(n) - stores index")
    
    print("\nWhen to use each:")
    print("  Linear Search:")
    print("    - Small datasets")
    print("    - Memory-constrained environments")
    print("    - One-time searches")
    
    print("\n  Dictionary Lookup:")
    print("    - Large datasets")
    print("    - Frequent searches")
    print("    - When speed is critical")
    
    print("\n" + "="*70)
    
    with open('docs/dsa_comparison_results.json', 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    print(f"\nResults saved to docs/dsa_comparison_results.json")
    print("="*70 + "\n")


if __name__ == '__main__':
    run_comparison()