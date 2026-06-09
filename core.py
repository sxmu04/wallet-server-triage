import json
import os
import time


DATA_FILE = os.path.join(os.path.dirname(__file__), "accounts.json")


def _ensure_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "ACC-001": {"titular": "Carlos Mendoza", "saldo": 500000.0, "estado": "ACTIVA", "historial": []},
                "ACC-002": {"titular": "Ana Gomez", "saldo": 12000.0, "estado": "ACTIVA", "historial": []},
                "ACC-003": {"titular": "Juan Perez", "saldo": 1000000.0, "estado": "BLOQUEADA", "historial": []}
            }, f, indent=4)


class AccountService:
    @staticmethod
    def get_account(account_id):
        _ensure_db()
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)

        if account_id in db:
            return db[account_id], 200
        return {"error": "Not Found"}, 404

    @staticmethod
    def change_status(acc_id, status_new):
        _ensure_db()
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)

        if acc_id in db:
            db[acc_id]["estado"] = status_new
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=4)
            return {"status": "CHANGED"}, 200

        return {"error": "Not Found"}, 404


class TransactionService:
    @staticmethod
    def transfer(origin, destiny, amount):
        _ensure_db()

        try:
            amount = float(amount)
        except Exception:
            return {"error": "Invalid amount"}, 422

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)

        if origin not in db or destiny not in db:
            return {"error": "Cuentas no encontradas"}, 404

        if db[origin]["estado"] != "ACTIVA":
            return {"error": "Cuenta de origen no disponible"}, 403

        if db[origin]["saldo"] < amount:
            return {"error": "Fondos insuficientes"}, 400

        # Simulate processing
        time.sleep(0.2)

        db[origin]["saldo"] -= amount
        db[destiny]["saldo"] += amount

        db[origin].setdefault("historial", []).append({"tipo": "DEBITO", "monto": amount, "target": destiny})
        db[destiny].setdefault("historial", []).append({"tipo": "CREDITO", "monto": amount, "target": origin})

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)

        return {"status": "SUCCESS", "message": "Transferencia procesada"}, 200
