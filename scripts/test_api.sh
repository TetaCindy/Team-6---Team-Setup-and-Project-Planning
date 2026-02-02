#!/bin/bash

# MoMo Transaction API Test Script
# Author: Mutoni Keira
# Tests all CRUD endpoints

BASE_URL="http://localhost:8000"
AUTH="admin:momo2024"

echo "======================================"
echo "MoMo Transaction API - Test Suite"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test 1: GET /transactions
echo "Test 1: GET /transactions (List all)"
response=$(curl -s -w "%{http_code}" $BASE_URL/transactions)
http_code="${response: -3}"
if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Status: $http_code"
else
    echo -e "${RED}✗ FAIL${NC} - Status: $http_code"
fi
echo ""

# Test 2: GET /transactions/1
echo "Test 2: GET /transactions/1 (Single transaction)"
response=$(curl -s -w "%{http_code}" $BASE_URL/transactions/1)
http_code="${response: -3}"
if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Status: $http_code"
else
    echo -e "${RED}✗ FAIL${NC} - Status: $http_code"
fi
echo ""

# Test 3: GET /transactions/9999 (Not found)
echo "Test 3: GET /transactions/9999 (Not found)"
response=$(curl -s -w "%{http_code}" $BASE_URL/transactions/9999)
http_code="${response: -3}"
if [ "$http_code" -eq 404 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Status: $http_code (expected 404)"
else
    echo -e "${RED}✗ FAIL${NC} - Status: $http_code"
fi
echo ""

# Test 4: POST /transactions
echo "Test 4: POST /transactions (Create new)"
response=$(curl -s -w "%{http_code}" -X POST $BASE_URL/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "test",
    "amount": "1000",
    "sender": "Test User",
    "receiver": "Test Receiver"
  }')
http_code="${response: -3}"
if [ "$http_code" -eq 201 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Status: $http_code"
    # Extract ID for next tests
    new_id=$(echo "$response" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
    echo "Created transaction ID: $new_id"
else
    echo -e "${RED}✗ FAIL${NC} - Status: $http_code"
fi
echo ""

# Test 5: PUT without auth (should fail)
echo "Test 5: PUT /transactions/1 (No auth - should fail)"
response=$(curl -s -w "%{http_code}" -X PUT $BASE_URL/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{"amount": "5000"}')
http_code="${response: -3}"
if [ "$http_code" -eq 401 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Status: $http_code (expected 401)"
else
    echo -e "${RED}✗ FAIL${NC} - Status: $http_code"
fi
echo ""

# Test 6: PUT with auth (should succeed)
echo "Test 6: PUT /transactions/1 (With auth)"
response=$(curl -s -w "%{http_code}" -X PUT $BASE_URL/transactions/1 \
  -u $AUTH \
  -H "Content-Type: application/json" \
  -d '{"amount": "6000"}')
http_code="${response: -3}"
if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Status: $http_code"
else
    echo -e "${RED}✗ FAIL${NC} - Status: $http_code"
fi
echo ""

# Test 7: DELETE without auth (should fail)
echo "Test 7: DELETE /transactions/$new_id (No auth - should fail)"
response=$(curl -s -w "%{http_code}" -X DELETE $BASE_URL/transactions/$new_id)
http_code="${response: -3}"
if [ "$http_code" -eq 401 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Status: $http_code (expected 401)"
else
    echo -e "${RED}✗ FAIL${NC} - Status: $http_code"
fi
echo ""

# Test 8: DELETE with auth (should succeed)
echo "Test 8: DELETE /transactions/$new_id (With auth)"
response=$(curl -s -w "%{http_code}" -X DELETE $BASE_URL/transactions/$new_id \
  -u $AUTH)
http_code="${response: -3}"
if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✓ PASS${NC} - Status: $http_code"
else
    echo -e "${RED}✗ FAIL${NC} - Status: $http_code"
fi
echo ""

echo "======================================"
echo "Test Suite Complete"
echo "======================================"
