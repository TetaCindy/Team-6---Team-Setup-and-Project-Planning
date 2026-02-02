# MoMo SMS REST API Documentation

## Base URL
```
http://localhost:8080
```

## Authentication
All endpoints require Basic Authentication.

**Credentials:**
- Username: `team6`
- Password: `team6`

**Header Format:**
```
Authorization: Basic dGVhbTY6dGVhbTY=
```

---

## Endpoints

### 1. Get All Transactions
Retrieve a list of all transactions.

**Endpoint:** `GET /transactions`

**Authentication:** Required

**Request Example:**
```bash
curl -u team6:team6 http://localhost:8080/transactions
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 12,
  "data": [
    {
      "id": 1,
      "transaction_id": "TXN000001",
      "sender": "Keira Mutoni",
      "sender_phone": "250788885125",
      "receiver": "Methode Duhujubumwe",
      "receiver_phone": "250790265770",
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
- `401 Unauthorized` - Invalid or missing credentials
- `500 Internal Server Error` - Server processing error

**Test Screenshot:** `get_all_transactions.png`

---

### 2. Get Single Transaction
Retrieve a specific transaction by ID.

**Endpoint:** `GET /transactions/{id}`

**Authentication:** Required

**Request Example:**
```bash
curl -u team6:team6 http://localhost:8080/transactions/1
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "transaction_id": "TXN000001",
    "sender": "Sylivie Tumukunde",
    "sender_phone": "250788749677",
    "receiver": "Cindy Teta",
    "receiver_phone": "250798200584",
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
- `401 Unauthorized` - Invalid or missing credentials
- `404 Not Found` - Transaction ID does not exist
- `500 Internal Server Error` - Server processing error

**Test Screenshot:** `get_single_transaction.png`

---

### 3. Create Transaction
Create a new transaction.

**Endpoint:** `POST /transactions`

**Authentication:** Required

**Required Fields:**
- `sender_phone` (string) - Sender's phone number
- `receiver_phone` (string) - Receiver's phone number  
- `amount` (number) - Transaction amount (must be > 0)

**Optional Fields:**
- `sender` (string) - Sender's name
- `receiver` (string) - Receiver's name
- `transaction_id` (string) - Custom transaction ID
- `transaction_type` (string) - Type: transfer, payment, airtime, etc.
- `status` (string) - Status: pending, completed, failed, cancelled
- `reference` (string) - Reference number
- `message` (string) - Transaction message/note

**Request Example:**
```bash
curl -u team6:team6 -X POST http://localhost:8080/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "Patrick Cyuzuzo",
    "sender_phone": "250783212343",
    "receiver": "Eric Izere",
    "receiver_phone": "2507986765421",
    "amount": 15000.0,
    "transaction_type": "transfer",
    "message": "Test transaction"
  }'
```

**Response (201 Created):**
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
- `400 Bad Request` - Missing required fields or invalid data
- `401 Unauthorized` - Invalid or missing credentials
- `500 Internal Server Error` - Server processing error

**Test Screenshot:** `post_create.png`

---

### 4. Update Transaction
Update an existing transaction.

**Endpoint:** `PUT /transactions/{id}`

**Authentication:** Required

**Request Example:**
```bash
curl -u team6:team6 -X PUT http://localhost:8080/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "pending",
    "message": "Updated message"
  }'
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Transaction updated successfully",
  "data": {
    "id": 1,
    "transaction_id": "TXN000001",
    "sender": "Methode Duhujubumwe",
    "sender_phone": "250790265770",
    "receiver": "Winebald Banituze",
    "receiver_phone": "250791829435",
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
- `400 Bad Request` - Invalid JSON format
- `401 Unauthorized` - Invalid or missing credentials
- `404 Not Found` - Transaction ID does not exist
- `500 Internal Server Error` - Server processing error

**Test Screenshot:** `put_update.png`

---

### 5. Delete Transaction
Delete a transaction by ID.

**Endpoint:** `DELETE /transactions/{id}`

**Authentication:** Required

**Request Example:**
```bash
curl -u team6:team6 -X DELETE http://localhost:8080/transactions/2
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Transaction 2 deleted successfully"
}
```

**Error Codes:**
- `401 Unauthorized` - Invalid or missing credentials
- `404 Not Found` - Transaction ID does not exist
- `500 Internal Server Error` - Server processing error

**Test Screenshot:** `delete_transaction.png`

---

### 6. Get Statistics (Bonus Endpoint)
Get transaction statistics and analytics.

**Endpoint:** `GET /stats`

**Authentication:** Required

**Request Example:**
```bash
curl -u team6:team6 http://localhost:8080/stats
```

**Response (200 OK):**
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

**Error Codes:**
- `401 Unauthorized` - Invalid or missing credentials
- `500 Internal Server Error` - Server processing error

---

## Authentication Security Analysis

### Basic Authentication Implementation
Our API uses HTTP Basic Authentication where credentials are Base64-encoded and sent in the Authorization header with each request. The server validates credentials before processing any operation.

### Critical Limitations of Basic Auth

#### 1. Credentials Transmitted in Every Request
Unlike token-based authentication where credentials are exchanged once for a session token, Basic Auth requires sending username and password with EVERY API call. For a mobile money application making hundreds of requests per session, credentials are exposed hundreds of times, creating multiple opportunities for interception.

#### 2. Base64 Encoding ≠ Encryption
Base64 is an ENCODING scheme, not encryption. Anyone with access to the Authorization header can decode it instantly:
```javascript
atob('dGVhbTY6dGVhbTY=')  // Returns: 'team6:team6'
```
Without HTTPS, credentials are effectively transmitted in plain text across the network.

#### 3. No Token Expiration
Credentials remain valid indefinitely until manually revoked. There is no automatic session timeout or expiration mechanism. If credentials are compromised, they can be used indefinitely until detected and changed.

#### 4. No Granular Access Control
Basic Auth provides only binary authentication (authenticated or not). It cannot enforce:
- Role-based access control (RBAC)
- Resource-level permissions
- Scope limitations
- Different access levels for different user types

#### 5. Vulnerable to Credential Stuffing
Static passwords enable credential stuffing attacks where attackers test leaked password databases against your API. Without built-in rate limiting or account lockout, unlimited authentication attempts are possible.

---

## Recommended Authentication Alternatives

### 1. JWT (JSON Web Tokens) - RECOMMENDED

**How JWT Works:**
1. User authenticates once with username/password
2. Server generates a cryptographically signed token containing user identity and permissions
3. Client stores token and sends it with subsequent requests
4. Server validates signature without database lookup
5. Token expires automatically (e.g., 15 minutes), forcing re-authentication

**Advantages:**
- ✓ Credentials sent only once during login
- ✓ Cryptographically signed (HMAC-SHA256 or RSA) - cannot be forged
- ✓ Built-in expiration (exp claim) limits damage from token theft
- ✓ Carries user roles and permissions in claims for granular access control
- ✓ Stateless validation - no database lookup needed, scales horizontally
- ✓ Refresh tokens enable session renewal without re-exposing passwords

**Example JWT Implementation:**
```bash
# Login endpoint returns JWT
POST /auth/login
{"username": "team6", "password": "team6"}
→ Response: {"access_token": "eyJhbGc...", "expires_in": 900}

# Subsequent requests use Bearer token
GET /transactions
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Token contains claims:
{
  "user_id": "12345",
  "role": "admin",
  "permissions": ["read", "write", "delete"],
  "exp": 1738534800  // Expires in 15 minutes
}
```

---

### 2. OAuth 2.0 - For Third-Party Access

**When to Use:**
OAuth 2.0 is the industry standard for third-party authorization. Use it when external applications (mobile apps, partner services) need access to user data without receiving the user's password.

**Key Features:**
- ✓ Scope-based permissions: Grant limited access (read-only, specific resources)
- ✓ Delegated authorization: User approves access without sharing password
- ✓ Multiple grant types: Authorization code (web), client credentials (server)
- ✓ Token revocation: Users can revoke third-party access anytime
- ✓ Widely supported: Used by Google, Facebook, GitHub for API access

**OAuth 2.0 Flow:**
```
1. App redirects user to: /oauth/authorize?client_id=ABC&scope=read_transactions
2. User approves access
3. Server redirects back with authorization code
4. App exchanges code for access token
5. App uses token to access API with limited scope
```

---

### 3. API Keys with HMAC Signatures

**Use Case:** Machine-to-machine communication (server-to-server)

**How it Works:**
- Each request includes a signature computed from the request body and a shared secret
- Prevents replay attacks
- Ensures request integrity
- Used by AWS, Stripe, and other major APIs

---

## Production Security Recommendations

For production deployment of the MoMo API, implement the following security measures:

### 1. Use HTTPS/TLS
- Deploy behind HTTPS reverse proxy (nginx, Apache)
- Use Let's Encrypt certificates
- Encrypt all data in transit

### 2. Implement JWT Authentication
**Configuration:**
- 15-minute access token expiration
- 7-day refresh token expiration
- RS256 algorithm for asymmetric signing
- Role-based claims (customer/agent/admin)
- Redis-based token blacklist for logout functionality

### 3. Add Rate Limiting
- IP-based rate limiting (100 requests/minute)
- User-based rate limiting
- Exponential backoff for failed authentication attempts
- Use Redis for distributed rate limiting

### 4. Database Integration
- Replace in-memory storage with PostgreSQL or MongoDB
- Use prepared statements to prevent SQL injection
- Implement connection pooling for performance
- Enable database encryption at rest

### 5. Comprehensive Logging & Monitoring
- Structured logging (JSON format)
- Log authentication failures
- Log all data modifications
- Monitor for suspicious activity patterns
- Use request IDs for tracing

### 6. Input Validation
- Validate all input using JSON schema validation
- Enforce business rules (maximum transaction limits)
- Sanitize string inputs to prevent injection attacks
- Type checking on all incoming data

### 7. API Key Rotation
- Implement automatic key rotation policies
- Provide API key management endpoints
- Allow users to revoke compromised keys

---

## Test Screenshots Reference

All test evidence is available in the `screenshots/` folder. Below are the actual test results captured from our implementation:

### 1. Successful_Authenticated_Request.png
Shows the server running and successfully handling authenticated GET requests. The server log displays:
```
Server running on http://localhost:8080
127.0.0.1 - - [02/Feb/2026 03:13:59] "GET /transactions HTTP/1.1" 200 -
127.0.0.1 - - [02/Feb/2026 03:19:57] "GET /transactions HTTP/1.1" 200 -
127.0.0.1 - - [02/Feb/2026 03:20:56] "GET /transactions HTTP/1.1" 200 -
```
**Demonstrates:** Server operational, successful authentication, 200 OK responses

---

### 2. Unauthorized_Request__Invalid_Credentials_.png
Shows 401 Unauthorized response when attempting to access API without valid credentials:
```bash
curl -v http://localhost:8080/transactions
```
**Response:**
```
HTTP/1.0 401 Unauthorized
WWW-Authenticate: Basic realm="Team 6"
{"error": "Unauthorized"}
```
**Demonstrates:** Proper authentication enforcement, WWW-Authenticate header, 401 status code

---

### 3. List_All_Transactions.png
Shows successful retrieval of all transactions with complete transaction data including:
- Transaction IDs (1686, 1687, 1688, 1689, 1690, 1691, 1692, 1693)
- Sender addresses: "M-Money"
- Transaction details with amounts (14,500 RWF, 6000 RWF, 27,000 RWF, 1,500 RWF, 24,900 RWF)
- Timestamps (14 Jan 2025, 15 Jan 2025, 16 Jan 2025)
- Balance information

**Demonstrates:** Successful data parsing from XML, complete transaction records, proper JSON formatting

---

### 4. View_Single_Transaction.png
Shows retrieval of a specific transaction by ID:
```bash
curl -u team6:team6 http://localhost:8080/transactions/1
```
**Response includes:**
```json
{
  "id": 1,
  "sender_address": "M-Money",
  "transaction_details": "You have received 2000 RWF from Jane Smith (*********013) 
                          on your mobile money account at 2024-05-10 16:30:51. 
                          Message from sender: . Your new balance:2000 RWF. 
                          Financial Transaction Id: 76662021700.",
  "timestamp": "10 May 2024 4:30:58 PM"
}
```
**Demonstrates:** GET by ID functionality, detailed transaction information, timestamp formatting

---

### 5. Add_New_Transaction.png
Shows successful POST request creating a new transaction:
```bash
curl -u team6:team6 -X POST -H "Content-Type: application/json" \
  -d '{"address": "0788111222", "body": "Team 6 Project Validation", 
       "readable_date": "1 Feb 2026", "id": 1693}' \
  http://localhost:8080/transactions
```
**Response:**
```json
{
  "address": "0788111222",
  "body": "Team 6 Project Validation",
  "readable_date": "1 Feb 2026",
  "id": 1693
}
```
**Demonstrates:** POST functionality, JSON request body processing, transaction creation with ID 1693

---

### 6. Update_Transaction.png
Shows successful PUT request updating an existing transaction:
```bash
curl -u team6:team6 -X PUT -H "Content-Type: application/json" \
  -d '{"body": "UPDATED MESSAGE FOR REPORT"}' \
  http://localhost:8080/transactions/1
```
**Response shows updated transaction:**
```json
{
  "id": 1,
  "sender_address": "M-Money",
  "transaction_details": "You have received 2000 RWF from Jane Smith (*********013) 
                          on your mobile money account at 2024-05-10 16:30:51. 
                          Message from sender: . Your new balance:2000 RWF. 
                          Financial Transaction Id: 76662021700.",
  "timestamp": "10 May 2024 4:30:58 PM",
  "body": "UPDATED MESSAGE FOR REPORT"
}
```
**Demonstrates:** PUT functionality, partial update capability, field modification

---

### 7. Delete_Transaction.png
Shows successful DELETE request removing a transaction:
```bash
curl -u team6:team6 -X DELETE http://localhost:8080/transactions/1
```
**Response:**
```json
{
  "message": "Deleted successfully"
}
```
**Demonstrates:** DELETE functionality, successful record removal, confirmation message

---

### 8. Performance_Results_and_Evidence.png
Shows the DSA performance comparison test results:
```bash
python3 etl/parse_to_json.py
python3 scripts/dsa_test.py
```
**Results:**
```
Successfully converted 1691 SMS records into outputs.json
---- Search Efficiency Results ----
Linear Search: 0.00000150s
Dictionary Lookup: 0.00000037s
Improvement: 4.00x faster
```
**Demonstrates:** 
- Successful XML parsing (1691 records converted)
- Linear search time: 0.0015 milliseconds
- Dictionary lookup time: 0.00037 milliseconds  
- Dictionary lookup is **4x faster** than linear search
- Validates the DSA comparison requirement

---

## Conclusion

This API demonstrates a complete RESTful implementation with CRUD operations, Basic Authentication security, and comprehensive error handling. While functional for development, production deployment requires migration to JWT or OAuth 2.0, HTTPS encryption, database persistence, rate limiting, and comprehensive logging to meet enterprise security standards for financial transaction systems.
