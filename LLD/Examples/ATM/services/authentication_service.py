"""
Authentication Service
Handles authentication logic and security validations
"""

import re
from typing import Optional
from models import Card


class AuthenticationService:
    """
    Authentication service following Single Responsibility Principle
    Handles all authentication-related operations
    """

    def __init__(self):
        self._max_pin_attempts = 3
        self._pin_patterns = [
            r"^\d{4}$",  # 4-digit PIN
            r"^\d{6}$",  # 6-digit PIN
        ]

        # Weak PIN patterns to reject
        self._weak_pins = {
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
            "1234",
            "4321",
            "0123",
            "2580",
            "1357",
            "2468",
        }

    def validate_pin_format(self, pin: str) -> bool:
        """
        Validate PIN format
        Returns True if PIN format is valid
        """
        if not pin:
            return False

        # Check if PIN matches any valid pattern
        for pattern in self._pin_patterns:
            if re.match(pattern, pin):
                return True

        return False

    def is_weak_pin(self, pin: str) -> bool:
        """
        Check if PIN is considered weak
        Returns True if PIN is weak
        """
        if not pin:
            return True

        # Check against known weak patterns
        if pin in self._weak_pins:
            return True

        # Check for sequential patterns
        if self._is_sequential(pin):
            return True

        return False

    def validate_card_number(self, card_number: str) -> bool:
        """
        Validate card number using Luhn algorithm
        Returns True if card number is valid
        """
        if not card_number or not card_number.isdigit():
            return False

        if len(card_number) not in [13, 14, 15, 16, 17, 18, 19]:
            return False

        return self._luhn_check(card_number)

    def authenticate_card(self, card: Card, pin: str) -> bool:
        """
        Authenticate card with PIN
        Returns True if authentication successful
        """
        if not card or not card.is_valid():
            return False

        if not self.validate_pin_format(pin):
            return False

        return card.verify_pin(pin)

    def is_card_expired(self, card: Card) -> bool:
        """
        Check if card is expired
        Returns True if card is expired
        """
        return card.is_expired() if card else True

    def can_attempt_authentication(self, card: Card) -> bool:
        """
        Check if authentication can be attempted
        Returns True if attempts are still allowed
        """
        if not card:
            return False

        return (
            card.failed_attempts < self._max_pin_attempts
            and not card.is_pin_locked
        )

    def _is_sequential(self, pin: str) -> bool:
        """Check if PIN has sequential digits"""
        if len(pin) < 3:
            return False

        # Check ascending sequence
        ascending = all(
            int(pin[i]) == int(pin[i - 1]) + 1 for i in range(1, len(pin))
        )

        # Check descending sequence
        descending = all(
            int(pin[i]) == int(pin[i - 1]) - 1 for i in range(1, len(pin))
        )

        return ascending or descending

    def _luhn_check(self, card_number: str) -> bool:
        """Implement Luhn algorithm for card number validation"""
        digits = [int(d) for d in card_number]

        # Double every second digit from right
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

        return sum(digits) % 10 == 0
