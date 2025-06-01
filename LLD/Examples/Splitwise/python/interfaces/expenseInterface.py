from abc import ABCMeta, abstractmethod


class Expense(ABCMeta):
    @abstractmethod
    def create_expense(self, amount, description, paid_by, paid_to):
        pass

    @abstractmethod
    def split_expense(self, group):
        pass

    @abstractmethod
    def show_expense(self):
        pass
