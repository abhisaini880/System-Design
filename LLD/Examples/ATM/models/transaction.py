"""
Transaction Model
Comprehensive transaction system with Command pattern and business logic
"""

from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass
import uuid
from abc import ABC, abstractmethod


class TransactionType(Enum):
    """Transaction types"""

    WITHDRAWAL = "WITHDRAWAL"
    DEPOSIT = "DEPOSIT"
    BALANCE_INQUIRY = "BALANCE_INQUIRY"
    TRANSFER = "TRANSFER"
    PIN_CHANGE = "PIN_CHANGE"


class TransactionStatus(Enum):
    """Transaction status"""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"


@dataclass
class TransactionResult:
    """Transaction result with comprehensive information"""

    success: bool
    transaction_id: str
    message: str
    error_code: Optional[str] = None
    balance_after: Optional[Decimal] = None
    receipt_data: Optional[Dict[str, Any]] = None


class Transaction:
    """
    Transaction entity implementing Command pattern
    Provides comprehensive transaction tracking and audit trail
    """

    def __init__(
        self,
        transaction_type: TransactionType,
        account_number: str,
        amount: Optional[Decimal] = None,
        description: str = "",
        reference_number: Optional[str] = None,
    ):
        self._transaction_id = str(uuid.uuid4())
        self._transaction_type = transaction_type
        self._account_number = account_number
        self._amount = amount or Decimal("0")
        self._description = description
        self._reference_number = (
            reference_number or self._generate_reference()
        )
        self._status = TransactionStatus.PENDING
        self._created_at = datetime.now()
        self._updated_at = self._created_at
        self._completed_at = None
        self._error_message = None
        self._error_code = None
        self._retry_count = 0
        self._max_retries = 3

        # Audit trail
        self._audit_trail = []
        self._add_audit_entry("Transaction created")

        # Transaction metadata
        self._metadata: Dict[str, Any] = {}

    @property
    def transaction_id(self) -> str:
        return self._transaction_id

    @property
    def transaction_type(self) -> TransactionType:
        return self._transaction_type

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def description(self) -> str:
        return self._description

    @property
    def reference_number(self) -> str:
        return self._reference_number

    @property
    def status(self) -> TransactionStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def completed_at(self) -> Optional[datetime]:
        return self._completed_at

    @property
    def error_message(self) -> Optional[str]:
        return self._error_message

    @property
    def retry_count(self) -> int:
        return self._retry_count

    def is_completed(self) -> bool:
        """Check if transaction is completed"""
        return self._status == TransactionStatus.COMPLETED

    def is_failed(self) -> bool:
        """Check if transaction failed"""
        return self._status == TransactionStatus.FAILED

    def can_retry(self) -> bool:
        """Check if transaction can be retried"""
        return (
            self._status == TransactionStatus.FAILED
            and self._retry_count < self._max_retries
        )

    def start_processing(self):
        """Mark transaction as processing"""
        if self._status == TransactionStatus.PENDING:
            self._status = TransactionStatus.PROCESSING
            self._updated_at = datetime.now()
            self._add_audit_entry("Transaction processing started")

    def complete_successfully(self, balance_after: Optional[Decimal] = None):
        """Mark transaction as completed successfully"""
        self._status = TransactionStatus.COMPLETED
        self._completed_at = datetime.now()
        self._updated_at = self._completed_at
        self._add_audit_entry("Transaction completed successfully")

        if balance_after is not None:
            self._metadata["balance_after"] = balance_after

    def fail_transaction(
        self, error_message: str, error_code: Optional[str] = None
    ):
        """Mark transaction as failed"""
        self._status = TransactionStatus.FAILED
        self._error_message = error_message
        self._error_code = error_code
        self._updated_at = datetime.now()
        self._add_audit_entry(f"Transaction failed: {error_message}")

    def cancel_transaction(self, reason: str = "User cancelled"):
        """Cancel transaction"""
        if self._status in [
            TransactionStatus.PENDING,
            TransactionStatus.PROCESSING,
        ]:
            self._status = TransactionStatus.CANCELLED
            self._error_message = reason
            self._updated_at = datetime.now()
            self._add_audit_entry(f"Transaction cancelled: {reason}")

    def timeout_transaction(self):
        """Mark transaction as timed out"""
        if self._status == TransactionStatus.PROCESSING:
            self._status = TransactionStatus.TIMEOUT
            self._error_message = "Transaction timed out"
            self._updated_at = datetime.now()
            self._add_audit_entry("Transaction timed out")

    def retry_transaction(self):
        """Retry failed transaction"""
        if self.can_retry():
            self._retry_count += 1
            self._status = TransactionStatus.PENDING
            self._error_message = None
            self._error_code = None
            self._updated_at = datetime.now()
            self._add_audit_entry(f"Transaction retry #{self._retry_count}")

    def add_metadata(self, key: str, value: Any):
        """Add metadata to transaction"""
        self._metadata[key] = value

    def get_metadata(self, key: str) -> Any:
        """Get metadata value"""
        return self._metadata.get(key)

    def get_audit_trail(self) -> list:
        """Get complete audit trail"""
        return self._audit_trail.copy()

    def get_duration_seconds(self) -> Optional[float]:
        """Get transaction duration in seconds"""
        if self._completed_at:
            return (self._completed_at - self._created_at).total_seconds()
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary for serialization"""
        return {
            "transaction_id": self._transaction_id,
            "transaction_type": self._transaction_type.value,
            "account_number": self._account_number,
            "amount": str(self._amount),
            "description": self._description,
            "reference_number": self._reference_number,
            "status": self._status.value,
            "created_at": self._created_at.isoformat(),
            "completed_at": (
                self._completed_at.isoformat() if self._completed_at else None
            ),
            "error_message": self._error_message,
            "error_code": self._error_code,
            "retry_count": self._retry_count,
            "metadata": self._metadata,
            "audit_trail": self._audit_trail,
        }

    def _generate_reference(self) -> str:
        """Generate unique reference number"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"REF{timestamp}{self._transaction_id[:8].upper()}"

    def _add_audit_entry(self, message: str):
        """Add entry to audit trail"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self._audit_trail.append(f"[{timestamp}] {message}")

    def __str__(self) -> str:
        return f"Transaction({self._transaction_id}, {self._transaction_type.value}, {self._status.value})"

    def __repr__(self) -> str:
        return self.__str__()


# Command Pattern Implementation for Transaction Operations
class TransactionCommand:
    """
    Abstract base class for transaction commands implementing Command pattern
    """

    def __init__(self, transaction: "Transaction", account: "Account"):
        self.transaction = transaction
        self.account = account

    def can_execute(self) -> bool:
        """Check if command can be executed"""
        raise NotImplementedError

    def execute(self) -> "TransactionResult":
        """Execute the command"""
        raise NotImplementedError


class WithdrawalCommand(TransactionCommand):
    """
    Command for withdrawal transactions
    """

    def __init__(
        self, transaction: "Transaction", account: "Account", cash_manager
    ):
        super().__init__(transaction, account)
        self.cash_manager = cash_manager

    def can_execute(self) -> bool:
        """Check if withdrawal can be executed"""
        if not self.account.is_active():
            return False

        if not self.account.can_withdraw(self.transaction.amount):
            return False

        if not self.cash_manager.can_dispense(self.transaction.amount):
            return False

        return True

    def execute(self) -> "TransactionResult":
        """Execute withdrawal"""
        try:
            self.transaction.start_processing()

            if self.account.withdraw(
                self.transaction.amount, "ATM Withdrawal"
            ):
                if self.cash_manager.dispense_cash(self.transaction.amount):
                    self.transaction.complete_successfully(
                        self.account.balance
                    )

                    return TransactionResult(
                        success=True,
                        transaction_id=self.transaction.transaction_id,
                        message="Withdrawal successful",
                        balance_after=self.account.balance,
                        receipt_data={
                            "amount": self.transaction.amount,
                            "balance": self.account.balance,
                            "transaction_date": self.transaction.created_at,
                        },
                    )
                else:
                    # Rollback account withdrawal
                    self.account.deposit(
                        self.transaction.amount, "ATM Withdrawal Rollback"
                    )
                    error_msg = "Cash dispensing failed"
                    self.transaction.fail_transaction(
                        error_msg, "CASH_DISPENSE_FAILED"
                    )
                    return TransactionResult(
                        success=False,
                        transaction_id=self.transaction.transaction_id,
                        message=error_msg,
                        error_code="CASH_DISPENSE_FAILED",
                    )
            else:
                error_msg = "Withdrawal failed"
                self.transaction.fail_transaction(
                    error_msg, "WITHDRAWAL_FAILED"
                )
                return TransactionResult(
                    success=False,
                    transaction_id=self.transaction.transaction_id,
                    message=error_msg,
                    error_code="WITHDRAWAL_FAILED",
                )

        except Exception as e:
            error_msg = f"Withdrawal error: {str(e)}"
            self.transaction.fail_transaction(error_msg, "SYSTEM_ERROR")
            return TransactionResult(
                success=False,
                transaction_id=self.transaction.transaction_id,
                message=error_msg,
                error_code="SYSTEM_ERROR",
            )


class DepositCommand(TransactionCommand):
    """
    Command for deposit transactions
    """

    def can_execute(self) -> bool:
        """Check if deposit can be executed"""
        if not self.account.is_active():
            return False

        if not self.account.can_deposit(self.transaction.amount):
            return False

        return True

    def execute(self) -> "TransactionResult":
        """Execute deposit"""
        try:
            self.transaction.start_processing()

            if self.account.deposit(self.transaction.amount, "ATM Deposit"):
                self.transaction.complete_successfully(self.account.balance)

                return TransactionResult(
                    success=True,
                    transaction_id=self.transaction.transaction_id,
                    message="Deposit successful",
                    balance_after=self.account.balance,
                    receipt_data={
                        "amount": self.transaction.amount,
                        "balance": self.account.balance,
                        "transaction_date": self.transaction.created_at,
                    },
                )
            else:
                error_msg = "Deposit failed"
                self.transaction.fail_transaction(error_msg, "DEPOSIT_FAILED")
                return TransactionResult(
                    success=False,
                    transaction_id=self.transaction.transaction_id,
                    message=error_msg,
                    error_code="DEPOSIT_FAILED",
                )

        except Exception as e:
            error_msg = f"Deposit error: {str(e)}"
            self.transaction.fail_transaction(error_msg, "SYSTEM_ERROR")
            return TransactionResult(
                success=False,
                transaction_id=self.transaction.transaction_id,
                message=error_msg,
                error_code="SYSTEM_ERROR",
            )


class BalanceInquiryCommand(TransactionCommand):
    """
    Command for balance inquiry transactions
    """

    def can_execute(self) -> bool:
        """Check if balance inquiry can be executed"""
        return self.account.is_active()

    def execute(self) -> "TransactionResult":
        """Execute balance inquiry"""
        try:
            self.transaction.start_processing()

            balance = self.account.balance
            self.transaction.complete_successfully(balance)

            return TransactionResult(
                success=True,
                transaction_id=self.transaction.transaction_id,
                message="Balance inquiry successful",
                balance_after=balance,
                receipt_data={
                    "balance": balance,
                    "transaction_date": self.transaction.created_at,
                },
            )

        except Exception as e:
            error_msg = f"Balance inquiry error: {str(e)}"
            self.transaction.fail_transaction(error_msg, "SYSTEM_ERROR")
            return TransactionResult(
                success=False,
                transaction_id=self.transaction.transaction_id,
                message=error_msg,
                error_code="SYSTEM_ERROR",
            )
