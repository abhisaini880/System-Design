"""
Account Model
Comprehensive account entity with proper encapsulation and business logic
"""

from decimal import Decimal
from datetime import datetime, date
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass, field
import uuid


class AccountType(Enum):
    """Account types with different privileges and limits"""

    SAVINGS = "SAVINGS"
    CHECKING = "CHECKING"
    BUSINESS = "BUSINESS"
    PREMIUM = "PREMIUM"


class AccountStatus(Enum):
    """Account status enumeration"""

    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"
    SUSPENDED = "SUSPENDED"


@dataclass
class AccountLimits:
    """Account limits configuration"""

    daily_withdrawal_limit: Decimal
    transaction_limit: Decimal
    minimum_balance: Decimal
    maximum_balance: Decimal = field(default=Decimal("1000000"))


class Account:
    """
    Account entity with comprehensive business logic
    Follows Single Responsibility and Open/Closed principles
    """

    def __init__(
        self,
        account_number: str,
        account_type: AccountType,
        holder_name: str,
        initial_balance: Decimal = Decimal("0"),
        limits: Optional[AccountLimits] = None,
    ):
        self._account_id = str(uuid.uuid4())
        self._account_number = account_number
        self._account_type = account_type
        self._holder_name = holder_name
        self._balance = initial_balance
        self._status = AccountStatus.ACTIVE
        self._created_at = datetime.now()
        self._last_transaction_date = None
        self._daily_withdrawal_amount = Decimal("0")
        self._daily_withdrawal_date = None

        # Set default limits based on account type
        self._limits = limits or self._get_default_limits()

        # Transaction history
        self._transaction_history: List[str] = []

    @property
    def account_id(self) -> str:
        return self._account_id

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def account_type(self) -> AccountType:
        return self._account_type

    @property
    def holder_name(self) -> str:
        return self._holder_name

    @property
    def balance(self) -> Decimal:
        return self._balance

    @property
    def status(self) -> AccountStatus:
        return self._status

    @property
    def limits(self) -> AccountLimits:
        return self._limits

    def is_active(self) -> bool:
        """Check if account is active for transactions"""
        return self._status == AccountStatus.ACTIVE

    def can_withdraw(self, amount: Decimal) -> bool:
        """Check if withdrawal is allowed"""
        if not self.is_active():
            return False

        if amount <= 0:
            return False

        if amount > self._limits.transaction_limit:
            return False

        if self._balance - amount < self._limits.minimum_balance:
            return False

        # Check daily withdrawal limit
        if self._is_same_day(self._daily_withdrawal_date):
            if (
                self._daily_withdrawal_amount + amount
                > self._limits.daily_withdrawal_limit
            ):
                return False

        return True

    def can_deposit(self, amount: Decimal) -> bool:
        """Check if deposit is allowed"""
        if not self.is_active():
            return False

        if amount <= 0:
            return False

        if amount > self._limits.transaction_limit:
            return False

        if self._balance + amount > self._limits.maximum_balance:
            return False

        return True

    def withdraw(self, amount: Decimal, description: str = "") -> bool:
        """Withdraw amount from account with proper validation"""
        if not self.can_withdraw(amount):
            return False

        self._balance -= amount
        self._update_daily_withdrawal(amount)
        self._add_transaction_record(f"WITHDRAWAL: -{amount} - {description}")
        self._last_transaction_date = datetime.now()

        return True

    def deposit(self, amount: Decimal, description: str = "") -> bool:
        """Deposit amount to account with proper validation"""
        if not self.can_deposit(amount):
            return False

        self._balance += amount
        self._add_transaction_record(f"DEPOSIT: +{amount} - {description}")
        self._last_transaction_date = datetime.now()

        return True

    def freeze_account(self, reason: str = "Security measure"):
        """Freeze account for security reasons"""
        self._status = AccountStatus.FROZEN
        self._add_transaction_record(f"ACCOUNT FROZEN: {reason}")

    def unfreeze_account(self):
        """Unfreeze account"""
        self._status = AccountStatus.ACTIVE
        self._add_transaction_record("ACCOUNT UNFROZEN")

    def get_daily_withdrawal_remaining(self) -> Decimal:
        """Get remaining daily withdrawal limit"""
        if not self._is_same_day(self._daily_withdrawal_date):
            return self._limits.daily_withdrawal_limit

        return (
            self._limits.daily_withdrawal_limit
            - self._daily_withdrawal_amount
        )

    def get_transaction_history(self, limit: int = 10) -> List[str]:
        """Get recent transaction history"""
        return self._transaction_history[-limit:]

    def _get_default_limits(self) -> AccountLimits:
        """Get default limits based on account type"""
        limits_map = {
            AccountType.SAVINGS: AccountLimits(
                daily_withdrawal_limit=Decimal("500"),
                transaction_limit=Decimal("1000"),
                minimum_balance=Decimal("100"),
            ),
            AccountType.CHECKING: AccountLimits(
                daily_withdrawal_limit=Decimal("1000"),
                transaction_limit=Decimal("2000"),
                minimum_balance=Decimal("0"),
            ),
            AccountType.BUSINESS: AccountLimits(
                daily_withdrawal_limit=Decimal("5000"),
                transaction_limit=Decimal("10000"),
                minimum_balance=Decimal("500"),
            ),
            AccountType.PREMIUM: AccountLimits(
                daily_withdrawal_limit=Decimal("10000"),
                transaction_limit=Decimal("25000"),
                minimum_balance=Decimal("1000"),
            ),
        }

        return limits_map.get(
            self._account_type, limits_map[AccountType.SAVINGS]
        )

    def _update_daily_withdrawal(self, amount: Decimal):
        """Update daily withdrawal tracking"""
        today = date.today()

        if not self._is_same_day(self._daily_withdrawal_date):
            self._daily_withdrawal_amount = Decimal("0")
            self._daily_withdrawal_date = today

        self._daily_withdrawal_amount += amount

    def _is_same_day(self, check_date: Optional[date]) -> bool:
        """Check if given date is today"""
        if check_date is None:
            return False
        return check_date == date.today()

    def _add_transaction_record(self, record: str):
        """Add transaction to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._transaction_history.append(f"[{timestamp}] {record}")

        # Keep only last 100 transactions in memory
        if len(self._transaction_history) > 100:
            self._transaction_history = self._transaction_history[-100:]

    def __str__(self) -> str:
        return f"Account({self._account_number}, {self._account_type.value}, Balance: ${self._balance})"

    def __repr__(self) -> str:
        return self.__str__()
