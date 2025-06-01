from abc import ABCMeta, abstractmethod


class Payment(ABCMeta):
    @abstractmethod
    def create_payment(self, amount, paid_by, paid_to, payment_method):
        pass

    @abstractmethod
    def settle_payment(self, group):
        pass
