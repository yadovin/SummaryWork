import datetime



class Transaction:
    def __init__(self,
                 amount : float,
                 category : str,
                 date : str,
                 description : str = "",
                 transaction_type : str = "expence"):
        if transaction_type not in ("expence", "income"):
            raise ValueError("Неверный тип транзакции.")

        if amount < 0:
            raise ValueError("Сумма транзакции должна быть положительной")

        self.amount = amount
        self.category = category.strip()
        self.date = self._validate_date(date)
        self.description = description.strip()
        self.transaction_type = transaction_type

    @staticmethod
    def _validate_date(date_str: str) -> str:
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValueError("Дата должна записываться в формате YYYY-MM-DD")


    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
            "transaction_type": self.transaction_type
        }