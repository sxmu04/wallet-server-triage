import json
import threading
import os

DATA_FILE = "accounts.json"
lock = threading.Lock()

class AccountRepository:

    @staticmethod
    def load_data():
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_data(data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)


class TransactionService:

    @staticmethod
    def validate_amount(amount):
        if not isinstance(amount, (int, float)):
            raise ValueError("Monto inválido")
        if amount <= 0:
            raise ValueError("Monto debe ser mayor a 0")

    @staticmethod
    def transfer(origin, destiny, amount):
        TransactionService.validate_amount(amount)

        with lock:  # 🔒 SOLUCIÓN A CONCURRENCIA
            db = AccountRepository.load_data()

            if origin not in db or destiny not in db:
                return {"error": "Cuentas no encontradas"}, 404

            if db[origin]["estado"] != "ACTIVA" or db[destiny]["estado"] != "ACTIVA":
                return {"error": "Cuenta bloqueada"}, 403

            if db[origin]["saldo"] < amount:
                return {"error": "Fondos insuficientes"}, 400

            # 💰 TRANSACCIÓN ATÓMICA
            db[origin]["saldo"] -= amount
            db[destiny]["saldo"] += amount

            db[origin]["historial"].append({
                "tipo": "DEBITO",
                "monto": amount,
                "target": destiny
            })

            db[destiny]["historial"].append({
                "tipo": "CREDITO",
                "monto": amount,
                "target": origin
            })

            AccountRepository.save_data(db)

        return {"status": "SUCCESS"}, 200


class AccountService:

    @staticmethod
    def get_account(account_id):
        db = AccountRepository.load_data()
        if account_id in db:
            return db[account_id], 200
        return {"error": "Not Found"}, 404

    @staticmethod
    def change_status(account_id, new_status):
        with lock:
            db = AccountRepository.load_data()

            if account_id not in db:
                return {"error": "Not Found"}, 404

            db[account_id]["estado"] = new_status
            AccountRepository.save_data(db)

        return {"status": "CHANGED"}, 200