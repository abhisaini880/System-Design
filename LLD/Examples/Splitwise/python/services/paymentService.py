from interfaces.paymentInterface import Payment as paymentInterface
from models.payment import Payment


class PaymentService(paymentInterface):
    def create_payment(self, amount, paid_by, paid_to, payment_method, group):
        self.payment = Payment(
            amount=amount,
            paid_by=paid_by,
            paid_to=paid_to,
            payment_method=payment_method,
        )

        self.group = group

        return self.payment

    def settle_payment(self):
        self.group.balances[self.payment.paid_by] = (
            self.group.balances[self.payment.paid_by] + self.payment.amount
        )
        self.group.balances[self.payment.paid_to] = (
            self.group.balances[self.payment.paid_to] - self.payment.amount
        )
