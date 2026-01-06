from datetime import datetime

class Operation:
    def __init__(self, amount, category, date, comment="", op_type="expense"):
        self.amount = amount
        self.category = category
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.comment = comment
        self.op_type = op_type

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date.strftime("%Y-%m-%d"),
            "comment": self.comment,
            "op_type": self.op_type
        }