"""
Enums and constants for ATM System
"""

from enum import Enum, auto
from decimal import Decimal


class ATMState(Enum):
    """ATM operational states"""

    IDLE = "idle"
    CARD_INSERTED = "card_inserted"
    AUTHENTICATED = "authenticated"
    TRANSACTION_IN_PROGRESS = "transaction_in_progress"
    MAINTENANCE = "maintenance"
    OUT_OF_ORDER = "out_of_order"


class TransactionType(Enum):
    """Types of transactions supported"""

    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    BALANCE_INQUIRY = "balance_inquiry"
    TRANSFER = "transfer"
    PIN_CHANGE = "pin_change"


class TransactionStatus(Enum):
    """Transaction processing status"""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AccountType(Enum):
    """Bank account types"""

    SAVINGS = "savings"
    CHECKING = "checking"
    CREDIT = "credit"
    BUSINESS = "business"


class CardType(Enum):
    """ATM card types"""

    DEBIT = "debit"
    CREDIT = "credit"
    PREPAID = "prepaid"


class CurrencyType(Enum):
    """Supported currencies"""

    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"


class ErrorCode(Enum):
    """System error codes"""

    INVALID_PIN = "E001"
    INSUFFICIENT_FUNDS = "E002"
    DAILY_LIMIT_EXCEEDED = "E003"
    CARD_EXPIRED = "E004"
    CARD_BLOCKED = "E005"
    NETWORK_ERROR = "E006"
    HARDWARE_FAILURE = "E007"
    INVALID_AMOUNT = "E008"
    TRANSACTION_TIMEOUT = "E009"
    MAINTENANCE_MODE = "E010"


# Transaction Limits
class TransactionLimits:
    """Transaction limits and constraints"""

    MAX_WITHDRAWAL_AMOUNT = Decimal("1000.00")
    MIN_WITHDRAWAL_AMOUNT = Decimal("10.00")
    DAILY_WITHDRAWAL_LIMIT = Decimal("2000.00")
    MAX_DEPOSIT_AMOUNT = Decimal("10000.00")
    MIN_DEPOSIT_AMOUNT = Decimal("1.00")
    MAX_TRANSFER_AMOUNT = Decimal("5000.00")

    # Session settings
    SESSION_TIMEOUT_SECONDS = 300  # 5 minutes
    MAX_PIN_ATTEMPTS = 3

    # Hardware constraints
    MAX_CASH_NOTES = 2000
    MIN_CASH_NOTES = 50
    RECEIPT_CHARACTER_LIMIT = 1000


# Currency Denominations
class CashDenominations:
    """Available cash denominations"""

    USD_DENOMINATIONS = [1, 5, 10, 20, 50, 100]
    EUR_DENOMINATIONS = [5, 10, 20, 50, 100, 200, 500]
    DEFAULT_DISPENSING_DENOMINATIONS = [
        20,
        50,
        100,
    ]  # Most common for dispensing


# System Configuration
class SystemConfig:
    """System-wide configuration constants"""

    ATM_ID_PREFIX = "ATM"
    TRANSACTION_ID_PREFIX = "TXN"
    RECEIPT_ID_PREFIX = "RCT"

    # Logging
    LOG_LEVEL = "INFO"
    AUDIT_LOG_RETENTION_DAYS = 2555  # 7 years

    # Security
    PIN_LENGTH = 4
    CARD_NUMBER_LENGTH = 16
    CVV_LENGTH = 3

    # Hardware timeouts
    CARD_READER_TIMEOUT = 30
    CASH_DISPENSER_TIMEOUT = 60
    RECEIPT_PRINTER_TIMEOUT = 30

    # Network
    BANK_API_TIMEOUT = 10
    MAX_RETRY_ATTEMPTS = 3

    # Display messages
    WELCOME_MESSAGE = "Welcome to SecureBank ATM"
    INSERT_CARD_MESSAGE = "Please insert your card"
    ENTER_PIN_MESSAGE = "Please enter your PIN"
    SELECT_TRANSACTION_MESSAGE = "Please select a transaction"
    REMOVE_CARD_MESSAGE = "Please remove your card"
    THANK_YOU_MESSAGE = "Thank you for using SecureBank ATM"


# Fee Structure
class FeeStructure:
    """Transaction fees configuration"""

    WITHDRAWAL_FEE = Decimal("2.50")
    BALANCE_INQUIRY_FEE = Decimal("0.00")
    TRANSFER_FEE = Decimal("1.00")
    FOREIGN_CARD_FEE = Decimal("3.00")
    OUT_OF_NETWORK_FEE = Decimal("2.00")


# Hardware Status
class HardwareStatus(Enum):
    """Hardware component status"""

    OPERATIONAL = "operational"
    MAINTENANCE_REQUIRED = "maintenance_required"
    OUT_OF_ORDER = "out_of_order"
    LOW_CASH = "low_cash"
    OUT_OF_PAPER = "out_of_paper"
    CARD_JAM = "card_jam"


class SecurityLevel(Enum):
    """Security levels for different operations"""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
