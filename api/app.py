"""
MoMo SMS REST API - Main Application
Complete implementation with Authentication and CRUD operations
Author: Cindy Saro Teta
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import base64
import os
from datetime import datetime
import urllib.parse

transactions = []
next_id = 1

VALID_USERNAME = "admin"
VALID_PASSWORD = "momo2024"


def load_transactions_from_xml():
    global transactions, next_id
    
    json_file = 'data/processed/transactions.json'
    
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                transactions = data.get('transactions', [])
                
                if transactions:
                    next_id = max(int(t.get('id', 0)) for t in transactions) + 1
                
                print(f"Loaded {len(transactions)} transactions from {json_file}")
        except Exception as e:
            print(f"Error loading transactions: {e}")
            transactions = []
    else:
        print(f"File not found: {json_file}")
        print("Creating sample transactions...")
        transactions = [
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
                "message": "Test transaction"
            },
            {
                "id": 2,
                "transaction_id": "TXN000002",
                "sender": "Alice Brown",
                "sender_phone": "250788999888",
                "receiver": "Bob Wilson",
                "receiver_phone": "250788777666",
                "amount": 10000.0,
                "transaction_type": "payment",
                "timestamp": "2024-01-16T09:15:00",
                "status": "completed",
                "reference": "REF002",
                "message": "Payment for services"
            }
        ]
        next_id = 3


class MoMoAPIHandler(BaseHTTPRequestHandler):
    
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def _authenticate(self):
        auth_header = self.headers.get('Authorization')
        
        if not auth_header:
            return False
        
        try:
            auth_type, credentials = auth_header.split(' ', 1)
            
            if auth_type.lower() != 'basic':
                return False
            
            decoded = base64.b64decode(credentials).decode('utf-8')
            username, password = decoded.split(':', 1)
            
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                return True
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
        
        return False
    
    def _send_json_response(self, data, status=200):
        self._set_headers(status)
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _send_error(self, message, status=400):
        self._send_json_response({
            'error': message,
            'status': status
        }, status)
    
    def _read_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        
        body = self.rfile.read(content_length)
        try:
            return json.loads(body.decode())
        except json.JSONDecodeError:
            return None
    
    def _parse_path(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        parts = path.strip('/').split('/')
        resource = parts[0] if parts else ''
        resource_id = None
        
        if len(parts) > 1 and parts[1].isdigit():
            resource_id = int(parts[1])
        
        return resource, resource_id
    
    def do_OPTIONS(self):
        self._set_headers(200)
    
    def do_GET(self):
        if not self._authenticate():
            self._send_error('Unauthorized - Invalid or missing credentials', 401)
            return
        
        resource, resource_id = self._parse_path()
        
        if resource == 'transactions':
            if resource_id:
                transaction = next((t for t in transactions if t['id'] == resource_id), None)
                
                if transaction:
                    self._send_json_response({
                        'success': True,
                        'data': transaction
                    })
                else:
                    self._send_error(f'Transaction with ID {resource_id} not found', 404)
            else:
                self._send_json_response({
                    'success': True,
                    'count': len(transactions),
                    'data': transactions
                })
        
        elif resource == 'stats':
            total_amount = sum(t.get('amount', 0) for t in transactions)
            avg_amount = total_amount / len(transactions) if transactions else 0
            
            status_count = {}
            for t in transactions:
                status = t.get('status', 'unknown')
                status_count[status] = status_count.get(status, 0) + 1
            
            self._send_json_response({
                'success': True,
                'data': {
                    'total_transactions': len(transactions),
                    'total_amount': total_amount,
                    'average_amount': round(avg_amount, 2),
                    'status_breakdown': status_count
                }
            })
        
        else:
            self._send_error('Resource not found', 404)
    
    def do_POST(self):
        if not self._authenticate():
            self._send_error('Unauthorized - Invalid or missing credentials', 401)
            return
        
        resource, _ = self._parse_path()
        
        if resource == 'transactions':
            data = self._read_body()
            
            if data is None:
                self._send_error('Invalid JSON in request body', 400)
                return
            
            required_fields = ['sender_phone', 'receiver_phone', 'amount']
            missing_fields = [f for f in required_fields if f not in data]
            
            if missing_fields:
                self._send_error(f'Missing required fields: {", ".join(missing_fields)}', 400)
                return
            
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    self._send_error('Amount must be greater than 0', 400)
                    return
            except (ValueError, TypeError):
                self._send_error('Invalid amount format', 400)
                return
            
            global next_id
            new_transaction = {
                'id': next_id,
                'transaction_id': data.get('transaction_id', f'TXN{next_id:06d}'),
                'sender': data.get('sender', ''),
                'sender_phone': data.get('sender_phone'),
                'receiver': data.get('receiver', ''),
                'receiver_phone': data.get('receiver_phone'),
                'amount': amount,
                'transaction_type': data.get('transaction_type', 'transfer'),
                'timestamp': data.get('timestamp', datetime.now().isoformat()),
                'status': data.get('status', 'completed'),
                'reference': data.get('reference', ''),
                'message': data.get('message', '')
            }
            
            transactions.append(new_transaction)
            next_id += 1
            
            self._send_json_response({
                'success': True,
                'message': 'Transaction created successfully',
                'data': new_transaction
            }, 201)
        
        else:
            self._send_error('Resource not found', 404)
    
    def do_PUT(self):
        if not self._authenticate():
            self._send_error('Unauthorized - Invalid or missing credentials', 401)
            return
        
        resource, resource_id = self._parse_path()
        
        if resource == 'transactions' and resource_id:
            data = self._read_body()
            
            if data is None:
                self._send_error('Invalid JSON in request body', 400)
                return
            
            transaction = next((t for t in transactions if t['id'] == resource_id), None)
            
            if not transaction:
                self._send_error(f'Transaction with ID {resource_id} not found', 404)
                return
            
            for key, value in data.items():
                if key != 'id':
                    transaction[key] = value
            
            transaction['updated_at'] = datetime.now().isoformat()
            
            self._send_json_response({
                'success': True,
                'message': 'Transaction updated successfully',
                'data': transaction
            })
        
        else:
            self._send_error('Invalid request - ID required for update', 400)
    
    def do_DELETE(self):
        if not self._authenticate():
            self._send_error('Unauthorized - Invalid or missing credentials', 401)
            return
        
        resource, resource_id = self._parse_path()
        
        if resource == 'transactions' and resource_id:
            global transactions
            
            original_count = len(transactions)
            transactions = [t for t in transactions if t['id'] != resource_id]
            
            if len(transactions) < original_count:
                self._send_json_response({
                    'success': True,
                    'message': f'Transaction {resource_id} deleted successfully'
                })
            else:
                self._send_error(f'Transaction with ID {resource_id} not found', 404)
        
        else:
            self._send_error('Invalid request - ID required for deletion', 400)
    
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {self.address_string()} - {format % args}")


def run_server(host='localhost', port=8000):
    load_transactions_from_xml()
    
    server_address = (host, port)
    httpd = HTTPServer(server_address, MoMoAPIHandler)
    
    print("\n" + "="*70)
    print("MoMo SMS REST API Server Started")
    print("="*70)
    print(f"Server: http://{host}:{port}/")
    print(f"Loaded: {len(transactions)} transactions")
    print("\nAPI Endpoints:")
    print("  GET    /transactions          - List all transactions")
    print("  GET    /transactions/{id}     - Get single transaction")
    print("  POST   /transactions          - Create new transaction")
    print("  PUT    /transactions/{id}     - Update transaction")
    print("  DELETE /transactions/{id}     - Delete transaction")
    print("  GET    /stats                 - Get statistics")
    print("\nAuthentication (Basic Auth):")
    print(f"  Username: {VALID_USERNAME}")
    print(f"  Password: {VALID_PASSWORD}")
    print("\nTest with curl:")
    print(f'  curl -u {VALID_USERNAME}:{VALID_PASSWORD} http://{host}:{port}/transactions')
    print("\nPress Ctrl+C to stop")
    print("="*70 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()
        print("Server stopped")


if __name__ == "__main__":
    run_server()