"""
Transaction Service
Handles all transaction processing with Command pattern implementation
"""

from decimal import Decimal
from typing import Optional
from models import (
    Transaction,
    TransactionResult,
    Account,
    WithdrawalCommand,
    DepositCommand,
    BalanceInquiryCommand,
)
from models.atm import CashManager


class TransactionService:
    """
    Transaction service implementing Command pattern
    Handles all transaction processing and validation
    """

    def __init__(self, cash_manager: Optional[CashManager] = None):
        self._cash_manager = cash_manager
        self._transaction_fee = Decimal(
            "0.00"
        )  # No fees for basic transactions

    def execute_withdrawal(
        self,
        transaction: Transaction,
        account: Account,
        cash_manager: CashManager,
    ) -> TransactionResult:
        """
        Execute withdrawal transaction using Command pattern
        """
        command = WithdrawalCommand(transaction, account, cash_manager)

        if not command.can_execute():
            transaction.fail_transaction(
                "Withdrawal cannot be executed", "WITHDRAWAL_BLOCKED"
            )
            return TransactionResult(
                success=False,
                transaction_id=transaction.transaction_id,
                message="Withdrawal cannot be executed",
                error_code="WITHDRAWAL_BLOCKED",
            )

        return command.execute()

    def execute_deposit(
        self, transaction: Transaction, account: Account
    ) -> TransactionResult:
        """
        Execute deposit transaction using Command pattern
        """
        command = DepositCommand(transaction, account)

        if not command.can_execute():
            transaction.fail_transaction(
                "Deposit cannot be executed", "DEPOSIT_BLOCKED"
            )
            return TransactionResult(
                success=False,
                transaction_id=transaction.transaction_id,
                message="Deposit cannot be executed",
                error_code="DEPOSIT_BLOCKED",
            )

        return command.execute()

    def execute_balance_inquiry(
        self, transaction: Transaction, account: Account
    ) -> TransactionResult:
        """
        Execute balance inquiry transaction using Command pattern
        """
        command = BalanceInquiryCommand(transaction, account)

        if not command.can_execute():
            transaction.fail_transaction(
                "Balance inquiry cannot be executed", "INQUIRY_BLOCKED"
            )
            return TransactionResult(
                success=False,
                transaction_id=transaction.transaction_id,
                message="Balance inquiry cannot be executed",
                error_code="INQUIRY_BLOCKED",
            )

        return command.execute()

    def execute_transfer(
        self,
        transaction: Transaction,
        from_account: Account,
        to_account: Account,
    ) -> TransactionResult:
        """
        Execute transfer transaction between accounts
        """
        try:
            transaction.start_processing()

            # Validate accounts
            if not from_account.is_active() or not to_account.is_active():
                error_msg = "One or both accounts are not active"
                transaction.fail_transaction(error_msg, "ACCOUNT_INACTIVE")
                return TransactionResult(
                    success=False,
                    transaction_id=transaction.transaction_id,
                    message=error_msg,
                    error_code="ACCOUNT_INACTIVE",
                )

            # Check if source account can withdraw
            if not from_account.can_withdraw(transaction.amount):
                error_msg = "Insufficient funds for transfer"
                transaction.fail_transaction(error_msg, "INSUFFICIENT_FUNDS")
                return TransactionResult(
                    success=False,
                    transaction_id=transaction.transaction_id,
                    message=error_msg,
                    error_code="INSUFFICIENT_FUNDS",
                )

            # Check if target account can receive deposit
            if not to_account.can_deposit(transaction.amount):
                error_msg = "Target account cannot receive deposit"
                transaction.fail_transaction(error_msg, "DEPOSIT_NOT_ALLOWED")
                return TransactionResult(
                    success=False,
                    transaction_id=transaction.transaction_id,
                    message=error_msg,
                    error_code="DEPOSIT_NOT_ALLOWED",
                )

            # Execute transfer (withdraw from source, deposit to target)
            if from_account.withdraw(
                transaction.amount, f"Transfer to {to_account.account_number}"
            ):
                if to_account.deposit(
                    transaction.amount,
                    f"Transfer from {from_account.account_number}",
                ):
                    transaction.complete_successfully(from_account.balance)

                    return TransactionResult(
                        success=True,
                        transaction_id=transaction.transaction_id,
                        message="Transfer successful",
                        balance_after=from_account.balance,
                        receipt_data={
                            "amount": transaction.amount,
                            "balance": from_account.balance,
                            "from_account": from_account.account_number,
                            "to_account": to_account.account_number,
                            "transaction_date": transaction.created_at,
                        },
                    )
                else:
                    # Rollback withdrawal
                    from_account.deposit(
                        transaction.amount, "Transfer rollback"
                    )
                    error_msg = "Transfer failed - deposit failed"
                    transaction.fail_transaction(error_msg, "TRANSFER_FAILED")
                    return TransactionResult(
                        success=False,
                        transaction_id=transaction.transaction_id,
                        message=error_msg,
                        error_code="TRANSFER_FAILED",
                    )
            else:
                error_msg = "Transfer failed - withdrawal failed"
                transaction.fail_transaction(error_msg, "TRANSFER_FAILED")
                return TransactionResult(
                    success=False,
                    transaction_id=transaction.transaction_id,
                    message=error_msg,
                    error_code="TRANSFER_FAILED",
                )

        except Exception as e:
            error_msg = f"Transfer error: {str(e)}"
            transaction.fail_transaction(error_msg, "SYSTEM_ERROR")
            return TransactionResult(
                success=False,
                transaction_id=transaction.transaction_id,
                message=error_msg,
                error_code="SYSTEM_ERROR",
            )

    def calculate_transaction_fee(
        self, transaction_type: str, amount: Decimal
    ) -> Decimal:
        """
        Calculate transaction fee based on type and amount
        Can be extended to implement different fee strategies
        """
        # For now, return zero fees
        # In a real system, this would implement complex fee calculations
        return Decimal("0.00")

    def validate_transaction_limits(
        self, account: Account, amount: Decimal
    ) -> bool:
        """
        Validate transaction against account limits
        """
        if not account.is_active():
            return False

        if amount <= 0:
            return False

        if amount > account.limits.transaction_limit:
            return False

        return True
