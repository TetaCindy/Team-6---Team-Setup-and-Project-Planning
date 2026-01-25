"""
API Testing Script
"""

import requests
import json

BASE_URL = "http://localhost:8000"
AUTH = ("admin", "momo2024")


def print_response(response, title):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")


def test_api():
    print("\n" + "="*60)
    print("Starting API Tests")
    print("="*60)
    
    print("\nTest 1: GET /transactions (Authenticated)")
    response = requests.get(f"{BASE_URL}/transactions", auth=AUTH)
    print_response(response, "GET All Transactions (Authenticated)")
    
    print("\nTest 2: GET /transactions (No Auth - Should Fail)")
    response = requests.get(f"{BASE_URL}/transactions")
    print_response(response, "GET All Transactions (No Auth)")
    
    print("\nTest 3: GET /transactions/1")
    response = requests.get(f"{BASE_URL}/transactions/1", auth=AUTH)
    print_response(response, "GET Single Transaction")
    
    print("\nTest 4: POST /transactions")
    new_transaction = {
        "sender": "Test Sender",
        "sender_phone": "250788111222",
        "receiver": "Test Receiver",
        "receiver_phone": "250788222333",
        "amount": 15000.0,
        "transaction_type": "transfer",
        "message": "API test transaction"
    }
    response = requests.post(
        f"{BASE_URL}/transactions",
        auth=AUTH,
        json=new_transaction
    )
    print_response(response, "POST New Transaction")
    
    print("\nTest 5: PUT /transactions/1")
    update_data = {
        "status": "pending",
        "message": "Updated via API"
    }
    response = requests.put(
        f"{BASE_URL}/transactions/1",
        auth=AUTH,
        json=update_data
    )
    print_response(response, "PUT Update Transaction")
    
    print("\nTest 6: DELETE /transactions/2")
    response = requests.delete(f"{BASE_URL}/transactions/2", auth=AUTH)
    print_response(response, "DELETE Transaction")
    
    print("\nTest 7: GET /stats")
    response = requests.get(f"{BASE_URL}/stats", auth=AUTH)
    print_response(response, "GET Statistics")
    
    print("\nTest 8: Wrong Password (Should Fail)")
    response = requests.get(
        f"{BASE_URL}/transactions",
        auth=("admin", "wrongpassword")
    )
    print_response(response, "Wrong Password")
    
    print("\n" + "="*60)
    print("API Tests Completed")
    print("="*60 + "\n")


if __name__ == "__main__":
    print("Make sure the API server is running on http://localhost:8000")
    input("Press Enter to start tests...")
    test_api()