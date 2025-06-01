"""
Card Model
Comprehensive card entity with security features and validation
"""

from datetime import datetime, date
from enum import Enum
from typing import Optional
import hashlib
import uuid
import re


class CardType(Enum):
    """Card types"""

    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
    PREPAID = "PREPAID"


class CardStatus(Enum):
    """Card status enumeration"""

    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"
    DAMAGED = "DAMAGED"


class Card:
    """
    Card entity with comprehensive security and validation
    Implements proper encapsulation and security best practices
    """

    def __init__(
        self,
        card_number: str,
        expiry_date: str,  # Format: MM/YY
        cvv: str,
        pin: str,
        card_type: CardType,
        account_number: str,
        holder_name: str,
    ):
        # Validate inputs
        self._validate_card_number(card_number)
        self._validate_expiry_date(expiry_date)
        self._validate_cvv(cvv)
        self._validate_pin(pin)

        self._card_id = str(uuid.uuid4())
        self._card_number = card_number
        self._expiry_date = expiry_date
        self._cvv_hash = self._hash_sensitive_data(cvv)
        self._pin_hash = self._hash_sensitive_data(pin)
        self._card_type = card_type
        self._account_number = account_number
        self._holder_name = holder_name
        self._status = CardStatus.ACTIVE
        self._created_at = datetime.now()
        self._last_used_at = None
        self._failed_attempts = 0
        self._max_failed_attempts = 3
        self._is_pin_locked = False

        # Track usage
        self._usage_count = 0
        self._daily_usage_count = 0
        self._last_usage_date = None

    @property
    def card_id(self) -> str:
        return self._card_id

    @property
    def card_number(self) -> str:
        return self._card_number

    @property
    def masked_card_number(self) -> str:
        """Return masked card number for display"""
        return f"****-****-****-{self._card_number[-4:]}"

    @property
    def expiry_date(self) -> str:
        return self._expiry_date

    @property
    def card_type(self) -> CardType:
        return self._card_type

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def holder_name(self) -> str:
        return self._holder_name

    @property
    def status(self) -> CardStatus:
        return self._status

    @property
    def failed_attempts(self) -> int:
        return self._failed_attempts

    @property
    def is_pin_locked(self) -> bool:
        return self._is_pin_locked

    def is_valid(self) -> bool:
        """Check if card is valid for transactions"""
        return (
            self._status == CardStatus.ACTIVE
            and not self.is_expired()
            and not self._is_pin_locked
        )

    def is_expired(self) -> bool:
        """Check if card has expired"""
        try:
            month, year = map(int, self._expiry_date.split("/"))
            # Convert YY to YYYY
            if year < 50:
                year += 2000
            else:
                year += 1900

            expiry = date(year, month, 1)
            # Card expires at end of month
            if expiry.month == 12:
                expiry = date(expiry.year + 1, 1, 1)
            else:
                expiry = date(expiry.year, expiry.month + 1, 1)

            return date.today() >= expiry
        except ValueError:
            return True

    def verify_pin(self, pin: str) -> bool:
        """Verify PIN with security measures"""
        if self._is_pin_locked:
            return False

        if self._hash_sensitive_data(pin) == self._pin_hash:
            self._failed_attempts = 0
            self._record_successful_usage()
            return True
        else:
            self._failed_attempts += 1
            if self._failed_attempts >= self._max_failed_attempts:
                self._is_pin_locked = True
                self._status = CardStatus.BLOCKED
            return False

    def verify_cvv(self, cvv: str) -> bool:
        """Verify CVV"""
        return self._hash_sensitive_data(cvv) == self._cvv_hash

    def change_pin(self, old_pin: str, new_pin: str) -> bool:
        """Change PIN with proper validation"""
        if not self.verify_pin(old_pin):
            return False

        try:
            self._validate_pin(new_pin)
            self._pin_hash = self._hash_sensitive_data(new_pin)
            return True
        except ValueError:
            return False

    def block_card(self, reason: str = "Security measure"):
        """Block card for security reasons"""
        self._status = CardStatus.BLOCKED

    def unblock_card(self):
        """Unblock card and reset failed attempts"""
        if self._status == CardStatus.BLOCKED:
            self._status = CardStatus.ACTIVE
            self._failed_attempts = 0
            self._is_pin_locked = False

    def suspend_card(self):
        """Temporarily suspend card"""
        self._status = CardStatus.SUSPENDED

    def activate_card(self):
        """Activate suspended card"""
        if self._status == CardStatus.SUSPENDED:
            self._status = CardStatus.ACTIVE

    def get_daily_usage_count(self) -> int:
        """Get today's usage count"""
        if self._last_usage_date != date.today():
            return 0
        return self._daily_usage_count

    def reset_pin_lock(self):
        """Reset PIN lock (admin function)"""
        self._is_pin_locked = False
        self._failed_attempts = 0
        if self._status == CardStatus.BLOCKED:
            self._status = CardStatus.ACTIVE

    def _record_successful_usage(self):
        """Record successful card usage"""
        self._last_used_at = datetime.now()
        self._usage_count += 1

        today = date.today()
        if self._last_usage_date != today:
            self._daily_usage_count = 1
            self._last_usage_date = today
        else:
            self._daily_usage_count += 1

    def _validate_card_number(self, card_number: str):
        """Validate card number using Luhn algorithm"""
        if not card_number or not card_number.isdigit():
            raise ValueError("Card number must contain only digits")

        if len(card_number) not in [13, 14, 15, 16, 17, 18, 19]:
            raise ValueError("Invalid card number length")

        # Luhn algorithm validation
        def luhn_check(card_num):
            digits = [int(d) for d in card_num]
            for i in range(len(digits) - 2, -1, -2):
                digits[i] *= 2
                if digits[i] > 9:
                    digits[i] -= 9
            return sum(digits) % 10 == 0

        if not luhn_check(card_number):
            raise ValueError("Invalid card number (failed Luhn check)")

    def _validate_expiry_date(self, expiry_date: str):
        """Validate expiry date format"""
        if not re.match(r"^\d{2}/\d{2}$", expiry_date):
            raise ValueError("Expiry date must be in MM/YY format")

        month, year = map(int, expiry_date.split("/"))
        if month < 1 or month > 12:
            raise ValueError("Invalid expiry month")

    def _validate_cvv(self, cvv: str):
        """Validate CVV"""
        if not cvv or not cvv.isdigit():
            raise ValueError("CVV must contain only digits")

        if len(cvv) not in [3, 4]:
            raise ValueError("CVV must be 3 or 4 digits")

    def _validate_pin(self, pin: str):
        """Validate PIN"""
        if not pin or not pin.isdigit():
            raise ValueError("PIN must contain only digits")

        if len(pin) not in [4, 6]:
            raise ValueError("PIN must be 4 or 6 digits")

        # Check for weak PINs
        if pin in [
            "0000",
            "1111",
            "2222",
            "3333",
            "4444",
            "5555",
            "6666",
            "7777",
            "8888",
            "9999",
        ]:
            raise ValueError("PIN cannot be all same digits")

        if pin in ["1234", "4321", "0123", "1111", "2580"]:
            raise ValueError("PIN is too common/weak")

    def _hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data using SHA-256"""
        return hashlib.sha256(f"{data}{self._card_id}".encode()).hexdigest()

    def __str__(self) -> str:
        return f"Card({self.masked_card_number}, {self._card_type.value}, {self._status.value})"

    def __repr__(self) -> str:
        return self.__str__()
