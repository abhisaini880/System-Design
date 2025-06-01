""" Settle Model Entity """


class Payment:
    def __init__(self, amount, paid_by, paid_to, payment_method):
        self.amount = amount
        self.paid_by = paid_by
        self.paid_to = paid_to
        self.payment_method = payment_method

    def get_amount(self):
        return self.amount

    def __repr__(self) -> str:
        return f"User {self.paid_by} paid  {self.amount} amount to user {self.paid_to} via {self.payment_method}"
