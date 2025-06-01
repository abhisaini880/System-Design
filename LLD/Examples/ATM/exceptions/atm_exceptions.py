"""
ATM System Exceptions
Custom exceptions for ATM operations with detailed error handling
"""

from typing import Optional
from enums.constants import ErrorCode


class ATMException(Exception):
    """Base exception for all ATM-related errors"""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        details: Optional[str] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.details = details
        super().__init__(f"{error_code.value}: {message}")


class AuthenticationException(ATMException):
    """Authentication-related exceptions"""

    pass


class InvalidPINException(AuthenticationException):
    """Raised when PIN is invalid"""

    def __init__(self, attempts_remaining: int):
        super().__init__(
            f"Invalid PIN. {attempts_remaining} attempts remaining.",
            ErrorCode.INVALID_PIN,
            f"attempts_remaining={attempts_remaining}",
        )
        self.attempts_remaining = attempts_remaining


class CardExpiredException(AuthenticationException):
    """Raised when card has expired"""

    def __init__(self, expiry_date: str):
        super().__init__(
            "Card has expired",
            ErrorCode.CARD_EXPIRED,
            f"expiry_date={expiry_date}",
        )


class CardBlockedException(AuthenticationException):
    """Raised when card is blocked"""

    def __init__(self, reason: str = "Card blocked"):
        super().__init__(
            reason, ErrorCode.CARD_BLOCKED, f"block_reason={reason}"
        )


class TransactionException(ATMException):
    """Transaction-related exceptions"""

    pass


class InsufficientFundsException(TransactionException):
    """Raised when account has insufficient funds"""

    def __init__(self, available_balance: float, requested_amount: float):
        super().__init__(
            f"Insufficient funds. Available: ${available_balance:.2f}, Requested: ${requested_amount:.2f}",
            ErrorCode.INSUFFICIENT_FUNDS,
            f"available={available_balance}, requested={requested_amount}",
        )
        self.available_balance = available_balance
        self.requested_amount = requested_amount


class DailyLimitExceededException(TransactionException):
    """Raised when daily transaction limit is exceeded"""

    def __init__(
        self,
        daily_limit: float,
        current_usage: float,
        requested_amount: float,
    ):
        super().__init__(
            f"Daily limit exceeded. Limit: ${daily_limit:.2f}, Used: ${current_usage:.2f}",
            ErrorCode.DAILY_LIMIT_EXCEEDED,
            f"limit={daily_limit}, used={current_usage}, requested={requested_amount}",
        )
        self.daily_limit = daily_limit
        self.current_usage = current_usage
        self.requested_amount = requested_amount


class InvalidAmountException(TransactionException):
    """Raised when transaction amount is invalid"""

    def __init__(self, amount: float, min_amount: float, max_amount: float):
        super().__init__(
            f"Invalid amount: ${amount:.2f}. Must be between ${min_amount:.2f} and ${max_amount:.2f}",
            ErrorCode.INVALID_AMOUNT,
            f"amount={amount}, min={min_amount}, max={max_amount}",
        )


class TransactionTimeoutException(TransactionException):
    """Raised when transaction times out"""

    def __init__(self, transaction_type: str, timeout_seconds: int):
        super().__init__(
            f"{transaction_type} transaction timed out after {timeout_seconds} seconds",
            ErrorCode.TRANSACTION_TIMEOUT,
            f"type={transaction_type}, timeout={timeout_seconds}",
        )


class HardwareException(ATMException):
    """Hardware-related exceptions"""

    pass


class CashDispenserException(HardwareException):
    """Raised when cash dispenser has issues"""

    def __init__(self, message: str = "Cash dispenser malfunction"):
        super().__init__(
            message, ErrorCode.HARDWARE_FAILURE, "component=cash_dispenser"
        )


class CardReaderException(HardwareException):
    """Raised when card reader has issues"""

    def __init__(self, message: str = "Card reader malfunction"):
        super().__init__(
            message, ErrorCode.HARDWARE_FAILURE, "component=card_reader"
        )


class ReceiptPrinterException(HardwareException):
    """Raised when receipt printer has issues"""

    def __init__(self, message: str = "Receipt printer malfunction"):
        super().__init__(
            message, ErrorCode.HARDWARE_FAILURE, "component=receipt_printer"
        )


class NetworkException(ATMException):
    """Network-related exceptions"""

    def __init__(self, message: str = "Network connection failed"):
        super().__init__(
            message, ErrorCode.NETWORK_ERROR, "network_failure=true"
        )


class MaintenanceModeException(ATMException):
    """Raised when ATM is in maintenance mode"""

    def __init__(self, estimated_duration: Optional[int] = None):
        message = "ATM is currently under maintenance"
        if estimated_duration:
            message += f". Estimated duration: {estimated_duration} minutes"

        super().__init__(
            message,
            ErrorCode.MAINTENANCE_MODE,
            f"duration={estimated_duration}" if estimated_duration else None,
        )
