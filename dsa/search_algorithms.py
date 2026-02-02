import time

def linear_search(transactions, transaction_id):
    """Search for transaction using linear search"""
    start_time = time.perf_counter()
    
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            end_time = time.perf_counter()
            return transaction, (end_time - start_time)
    
    end_time = time.perf_counter()
    return None, (end_time - start_time)

def dictionary_lookup(transaction_dict, transaction_id):
    """Search for transaction using dictionary lookup"""
    start_time = time.perf_counter()
    
    result = transaction_dict.get(transaction_id)
    
    end_time = time.perf_counter()
    return result, (end_time - start_time)

def create_transaction_dict(transactions):
    """Convert list to dictionary for O(1) lookup"""
    return {trans['id']: trans for trans in transactions}
