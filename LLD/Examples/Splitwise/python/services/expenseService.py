from interfaces.expenseInterface import Expense as expenseInterface
from models.expense import Expense
from models.group import Group


class ExpenseService(expenseInterface):
    def create_expense(self, amount, desciption, paid_by, group: Group):
        self.expense = Expense(
            amount=amount, description=desciption, paid_by=paid_by
        )
        self.group = group

        return self.expense

    def split_expense(self):
        share = self.expense.amount / len(self.group.members)
        for member, balance in self.group.balances.items():
            if member != self.expense.paid_by:
                self.group.balances[member] = balance - share
            else:
                self.group.balances[member] = balance + share
