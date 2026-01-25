import json
from http.server import HTTPServer, BaseHTTPRequestHandler

transactions = [
    {"id": "1", "type": "Transfer", "amount": 1000.0, "sender": "John", "receiver": "Doe", "timestamp": "2026-01-25 10:00:00"}
]

class MoMoAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/transactions':
            self._set_headers(200)
            self.wfile.write(json.dumps(transactions).encode())
        
        elif self.path.startswith('/transactions/'):
            tx_id = self.path.split('/')[-1]
            transaction = next((t for t in transactions if t['id'] == tx_id), None)
            if transaction:
                self._set_headers(200)
                self.wfile.write(json.dumps(transaction).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())

    def do_POST(self):
        if self.path == '/transactions':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            transactions.append(post_data)
            self._set_headers(201)
            self.wfile.write(json.dumps({"message": "Transaction created"}).encode())

    def do_PUT(self):
        if self.path.startswith('/transactions/'):
            tx_id = self.path.split('/')[-1]
            content_length = int(self.headers['Content-Length'])
            put_data = json.loads(self.rfile.read(content_length))
            
            for t in transactions:
                if t['id'] == tx_id:
                    t.update(put_data)
                    self._set_headers(200)
                    self.wfile.write(json.dumps(t).encode())
                    return
            self._set_headers(404)

    def do_DELETE(self):
        if self.path.startswith('/transactions/'):
            tx_id = self.path.split('/')[-1]
            global transactions
            transactions = [t for t in transactions if t['id'] != tx_id]
            self._set_headers(200)
            self.wfile.write(json.dumps({"message": "Deleted"}).encode())

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MoMoAPIHandler)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
