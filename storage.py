import os
import csv
from models import Operation


DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "operations.csv")

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def save_operations(operations: list[Operation], overwrite=False):
    ensure_data_dir()
    mode = 'w' if overwrite else 'a'
    with open(CSV_FILE, mode=mode, newline='', encoding='utf-8') as f:
        fieldnames = ["amount", "category", "date", "comment", "op_type"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if overwrite:
            writer.writeheader()
        for op in operations:
            writer.writerow(op.to_dict())

def load_operations() -> list[Operation]:

    operations = []

    if not os.path.exists(CSV_FILE):
        return operations

    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    op = Operation(
                        amount=float(row["amount"]),
                        category=row["category"],
                        date=row["date"],
                        comment=row.get("comment", ""),
                        op_type=row["op_type"]
                    )
                    operations.append(op)
                except ValueError as ve:
                    print(f"Пропущена некорректная запись: {ve}")

    except (IOError, csv.Error) as e:
        print(f"Ошибка при загрузке данных: {e}")

    return operations