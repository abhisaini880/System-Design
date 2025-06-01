""" Expense Model Entity """


class Expense:
    def __init__(self, amount, description, paid_by):
        self.amount = amount
        self.description = description
        self.paid_by = paid_by

    def __repr__(self) -> str:
        return f"Amount: {self.amount} for {self.description} paid by {self.paid_by.name}"
