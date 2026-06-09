import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

DATA_FILE = "accounts.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({
            "ACC-001": {"titular": "Carlos Mendoza", "saldo": 500000.0, "estado": "ACTIVA", "historial": []},
            "ACC-002": {"titular": "Ana Gomez", "saldo": 12000.0, "estado": "ACTIVA", "historial": []},
            "ACC-003": {"titular": "Juan Perez", "saldo": 1000000.0, "estado": "BLOQUEADA", "historial": []}
        }, f, indent=4)

class PaymentGatewayAPI(BaseHTTPRequestHandler):

    def _response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        url_parsed = urlparse(self.path)
        path = url_parsed.path
        query = parse_qs(url_parsed.query)

        if path == "/api/v1/accounts/detail":
            account_id = query.get("id")[0] 
            
            with open(DATA_FILE, "r") as f:
                db = json.load(f)

            if account_id in db:
                self._response(db[account_id])
            else:
                self._response({"error": "Not Found"}, 404)
        else:
            self._response({"msg": "Gateway Ready"}, 200)

    def do_POST(self):
        url_parsed = urlparse(self.path)
        path = url_parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            return self._response({"error": "Bad Request JSON"}, 400)

        if path == "/api/v1/transactions/transfer":
            origin = payload.get("desde")
            destiny = payload.get("hacia")
            amount = payload.get("monto") 

            with open(DATA_FILE, "r") as f:
                db = json.load(f)

            if origin in db and destiny in db:
                if db[origin]["estado"] == "ACTIVA":
                    if db[origin]["saldo"] >= amount:
                        
                        time.sleep(0.5) 

                        db[origin]["saldo"] -= amount
                        db[destiny]["saldo"] += amount

                        db[origin]["historial"].append({"tipo": "DEBITO", "monto": amount, "target": destiny})
                        db[destiny]["historial"].append({"tipo": "CREDITO", "monto": amount, "target": origin})

                        with open(DATA_FILE, "w") as f:
                            json.dump(db, f, indent=4)

                        return self._response({"status": "SUCCESS", "message": "Transferencia procesada"})
                    else:
                        return self._response({"error": "Fondos insuficientes"}, 400)
                else:
                    return self._response({"error": "Cuenta de origen no disponible"}, 403)
            else:
                return self._response({"error": "Cuentas no encontradas"}, 404)

        elif path == "/api/v1/accounts/admin/bypass-status":
            acc_id = payload.get("id")
            new_status = payload.get("status")
            
            with open(DATA_FILE, "r") as f:
                db = json.load(f)
                
            if acc_id in db:
                db[acc_id]["estado"] = new_status
                with open(DATA_FILE, "w") as f:
                    json.dump(db, f, indent=4)
                return self._response({"status": "CHANGED"})
            
            return self._response({"error": "Not Found"}, 404)

        self._response({"error": "Endpoint inválido"}, 404)

def run(port=8500):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PaymentGatewayAPI)
    print(f"💰 Core Bancario / API Gateway corriendo en puerto {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == "__main__":
    run()