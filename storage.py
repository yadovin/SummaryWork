import os
import csv

from models import Transaction

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "transactions.csv")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_transactions(transactions):
    if not transactions: return
    ensure_data_dir()
    file_exists = os.path.isfile(CSV_FILE)
    try:
        with open(CSV_FILE, mode = "a", newline="", encoding="utf-8") as f:
            fieldnames = ['amount', 'category', 'date', 'description', 'transaction_type']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for t in transactions:
                writer.writerow(t.to_dict())

    except Exception as e:
        print(f"Ошибка при сохранении данных {e}")

def load_transactions():
    transactions = []
    if not os.path.isfile(DATA_DIR):
        return transactions
    try:
        with open(CSV_FILE, mode = "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                t = Transaction(
                    amount=float(row['amount']),
                    category=row['category'],
                    date=row['date'],
                    description=row.get('description', ''),
                    transaction_type=row['transaction_type']
                )
                transactions.append(t)

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return []
    return transactions




