import json
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

DATA_FILE = 'data/transactions.json'

USER_AUTH = "team6"
PASS_AUTH = "team6"


def load_db():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_db(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


class TransactionAPI(BaseHTTPRequestHandler):

    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # indent=4 ensures the terminal output is easy to read for screenshots
        self.wfile.write(json.dumps(data, indent=4).encode())

    def check_auth(self):
        auth_header = self.headers.get('Authorization')
        if auth_header and auth_header.startswith('Basic '):
            encoded_creds = auth_header.split(' ')[1]
            decoded_creds = base64.b64decode(encoded_creds).decode().split(':')
            if decoded_creds[0] == USER_AUTH and decoded_creds[1] == PASS_AUTH:
                return True

        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Team 6 API"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
        return False

    def do_GET(self):
        if not self.check_auth():
            return
        db = load_db()
        if self.path == '/transactions':
            self.send_json_response(200, db)
        elif self.path.startswith('/transactions/'):
            try:
                tx_id = int(self.path.split('/')[-1])
                # Task 5: Linear search implementation
                record = next((t for t in db if t['id'] == tx_id), None)
                if record:
                    self.send_json_response(200, record)
                else:
                    self.send_json_response(404, {"error": "Not found"})
            except ValueError:
                self.send_json_response(400, {"error": "Invalid ID format"})

    def do_POST(self):
        if not self.check_auth():
            return
        if self.path == '/transactions':
            length = int(self.headers['Content-Length'])
            new_data = json.loads(self.rfile.read(length))
            db = load_db()
            new_data['id'] = max(t['id'] for t in db) + 1 if db else 1
            db.append(new_data)
            save_db(db)
            self.send_json_response(201, new_data)

    def do_PUT(self):
        if not self.check_auth():
            return
        if self.path.startswith('/transactions/'):
            tx_id = int(self.path.split('/')[-1])
            length = int(self.headers['Content-Length'])
            updates = json.loads(self.rfile.read(length))
            db = load_db()
            for t in db:
                if t['id'] == tx_id:
                    t.update(updates)
                    save_db(db)
                    return self.send_json_response(200, t)
            self.send_json_response(404, {"error": "Not found"})

    def do_DELETE(self):
        if not self.check_auth():
            return
        if self.path.startswith('/transactions/'):
            tx_id = int(self.path.split('/')[-1])
            db = load_db()
            filtered_db = [t for t in db if t['id'] != tx_id]
            if len(filtered_db) < len(db):
                save_db(filtered_db)
                self.send_json_response(
                    200, {"message": "Deleted successfully"})
            else:
                self.send_json_response(404, {"error": "Not found"})


if __name__ == "__main__":
    server = HTTPServer(('localhost', 8080), TransactionAPI)
    print("Server running on http://localhost:8080")
    server.serve_forever()
