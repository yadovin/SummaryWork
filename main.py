from models import Transaction
from storage import save_transactions, load_transactions

def main():
    print("Загрузка операций: ")
    transactions = load_transactions()
    print(f"Загружено {len(transactions)} транзакций")

    if len(transactions) == 0:
        t1=Transaction(200, "кофе", "2025-12-23", "комментарий")
        t2=Transaction(50000, "зп", "2025-12-01", "Аванс", "income")
        save_transactions([t1,t2])
        transactions = [t1,t2]
    else:
        print("Операции уже есть")

    for t in transactions:
        print(t)


if __name__ == "__main__":
    main()
