# MoMo SMS REST API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints require Basic Authentication.

**Credentials:**
- Username: `admin`
- Password: `momo2024`

**Header Format:**
```
Authorization: Basic YWRtaW46bW9tbzIwMjQ=
```

## Endpoints

### 1. Get All Transactions
Retrieve a list of all transactions.

**Endpoint:** `GET /transactions`

**Request Example:**
```bash
curl -u admin:momo2024 http://localhost:8000/transactions
```

**Response Example:**
```json
{
  "success": true,
  "count": 12,
  "data": [
    {
      "id": 1,
      "transaction_id": "TXN000001",
      "sender": "John Doe",
      "sender_phone": "250788123456",
      "receiver": "Jane Smith",
      "receiver_phone": "250788654321",
      "amount": 5000.0,
      "transaction_type": "transfer",
      "timestamp": "2024-01-15T14:30:00",
      "status": "completed",
      "reference": "REF001",
      "message": "Money transfer"
    }
  ]
}
```

**Error Codes:**
- `401`: Unauthorized - Invalid or missing credentials
- `500`: Internal server error

---

### 2. Get Single Transaction
Retrieve a specific transaction by ID.

**Endpoint:** `GET /transactions/{id}`

**Request Example:**
```bash
curl -u admin:momo2024 http://localhost:8000/transactions/1
```

**Response Example:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "transaction_id": "TXN000001",
    "sender": "John Doe",
    "sender_phone": "250788123456",
    "receiver": "Jane Smith",
    "receiver_phone": "250788654321",
    "amount": 5000.0,
    "transaction_type": "transfer",
    "timestamp": "2024-01-15T14:30:00",
    "status": "completed",
    "reference": "REF001",
    "message": "Money transfer"
  }
}
```

**Error Codes:**
- `401`: Unauthorized
- `404`: Transaction not found
- `500`: Internal server error

---

### 3. Create Transaction
Create a new transaction.

**Endpoint:** `POST /transactions`

**Request Example:**
```bash
curl -u admin:momo2024 -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "New Sender",
    "sender_phone": "250788111222",
    "receiver": "New Receiver",
    "receiver_phone": "250788222333",
    "amount": 15000.0,
    "transaction_type": "transfer",
    "message": "Test transaction"
  }'
```

**Required Fields:**
- `sender_phone` (string)
- `receiver_phone` (string)
- `amount` (number, must be > 0)

**Optional Fields:**
- `sender` (string)
- `receiver` (string)
- `transaction_id` (string)
- `transaction_type` (string: transfer, payment, airtime, etc.)
- `status` (string: pending, completed, failed, cancelled)
- `reference` (string)
- `message` (string)

**Response Example:**
```json
{
  "success": true,
  "message": "Transaction created successfully",
  "data": {
    "id": 13,
    "transaction_id": "TXN000013",
    "sender": "New Sender",
    "sender_phone": "250788111222",
    "receiver": "New Receiver",
    "receiver_phone": "250788222333",
    "amount": 15000.0,
    "transaction_type": "transfer",
    "timestamp": "2024-01-25T14:30:00",
    "status": "completed",
    "reference": "",
    "message": "Test transaction"
  }
}
```

**Error Codes:**
- `400`: Bad request - Missing required fields or invalid data
- `401`: Unauthorized
- `500`: Internal server error

---

### 4. Update Transaction
Update an existing transaction.

**Endpoint:** `PUT /transactions/{id}`

**Request Example:**
```bash
curl -u admin:momo2024 -X PUT http://localhost:8000/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "pending",
    "message": "Updated message"
  }'
```

**Response Example:**
```json
{
  "success": true,
  "message": "Transaction updated successfully",
  "data": {
    "id": 1,
    "transaction_id": "TXN000001",
    "sender": "John Doe",
    "sender_phone": "250788123456",
    "receiver": "Jane Smith",
    "receiver_phone": "250788654321",
    "amount": 5000.0,
    "transaction_type": "transfer",
    "timestamp": "2024-01-15T14:30:00",
    "status": "pending",
    "reference": "REF001",
    "message": "Updated message",
    "updated_at": "2024-01-25T15:00:00"
  }
}
```

**Error Codes:**
- `400`: Bad request - Invalid JSON
- `401`: Unauthorized
- `404`: Transaction not found
- `500`: Internal server error

---

### 5. Delete Transaction
Delete a transaction.

**Endpoint:** `DELETE /transactions/{id}`

**Request Example:**
```bash
curl -u admin:momo2024 -X DELETE http://localhost:8000/transactions/2
```

**Response Example:**
```json
{
  "success": true,
  "message": "Transaction 2 deleted successfully"
}
```

**Error Codes:**
- `401`: Unauthorized
- `404`: Transaction not found
- `500`: Internal server error

---

### 6. Get Statistics
Get transaction statistics (bonus endpoint).

**Endpoint:** `GET /stats`

**Request Example:**
```bash
curl -u admin:momo2024 http://localhost:8000/stats
```

**Response Example:**
```json
{
  "success": true,
  "data": {
    "total_transactions": 12,
    "total_amount": 98200.0,
    "average_amount": 8183.33,
    "status_breakdown": {
      "completed": 10,
      "pending": 1,
      "failed": 1
    }
  }
}
```

---

## Security Notes

### Basic Authentication Limitations
Basic Authentication is used in this implementation for simplicity, but it has significant security weaknesses:

1. **Credentials transmitted in Base64**: Base64 is encoding, not encryption. Credentials can be easily decoded.
2. **No token expiration**: Credentials are sent with every request, increasing exposure.
3. **Vulnerable to interception**: Without HTTPS, credentials can be intercepted.
4. **No granular permissions**: Cannot implement role-based access control easily.

### Recommended Alternatives

#### JWT (JSON Web Tokens)
- Tokens expire after a set time
- Can include user roles and permissions
- Stateless authentication
- Industry standard

#### OAuth 2.0
- Delegated authorization
- No password sharing
- Fine-grained access control
- Used by major platforms (Google, Facebook, etc.)

### Production Recommendations
1. Use HTTPS/TLS for all communication
2. Implement JWT or OAuth 2.0
3. Add rate limiting
4. Implement API key rotation
5. Use secure password hashing (bcrypt, Argon2)
6. Add request validation and sanitization
7. Implement comprehensive logging and monitoring