from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

from core import TransactionService, AccountService

# 🔐 TOKEN SIMULADO
ADMIN_TOKEN = "SECURE123"


class SecurityMiddleware:

    @staticmethod
    def validate_admin(headers):
        token = headers.get("Authorization")
        if token != ADMIN_TOKEN:
            return False
        return True


class PaymentGatewayAPI(BaseHTTPRequestHandler):

    def _response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/v1/accounts/detail":
            account_id = query.get("id", [None])[0]

            if not account_id:
                return self._response({"error": "Missing ID"}, 400)

            data, status = AccountService.get_account(account_id)
            return self._response(data, status)

        return self._response({"msg": "API Running"}, 200)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body.decode())
        except:
            return self._response({"error": "Bad JSON"}, 400)

        # 💸 TRANSFERENCIA
        if path == "/api/v1/transactions/transfer":
            origin = payload.get("desde")
            destiny = payload.get("hacia")
            amount = payload.get("monto")

            if not origin or not destiny or amount is None:
                return self._response({"error": "Datos incompletos"}, 422)

            data, status = TransactionService.transfer(origin, destiny, amount)
            return self._response(data, status)

        # 🔐 ADMIN PROTEGIDO
        if path == "/api/v1/accounts/admin/bypass-status":

            if not SecurityMiddleware.validate_admin(self.headers):
                return self._response({"error": "Unauthorized"}, 401)

            acc_id = payload.get("id")
            status_new = payload.get("status")

            if not acc_id or not status_new:
                return self._response({"error": "Datos incompletos"}, 422)

            data, status = AccountService.change_status(acc_id, status_new)
            return self._response(data, status)

        return self._response({"error": "Endpoint inválido"}, 404)


def run(port=8500):
    server = HTTPServer(("", port), PaymentGatewayAPI)
    print(f"🚀 SecureWallet corriendo en puerto {port}")
    server.serve_forever()


if __name__ == "__main__":
    run()