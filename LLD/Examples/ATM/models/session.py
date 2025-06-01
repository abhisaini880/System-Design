"""
ATM Session Model
Manages user sessions with timeout and security features
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
import uuid


class SessionStatus(Enum):
    """Session status enumeration"""

    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    TERMINATED = "TERMINATED"
    LOCKED = "LOCKED"


class ATMSession:
    """
    ATM Session management with security features
    Handles session lifecycle, timeouts, and security measures
    """

    def __init__(
        self, card_number: str, account_number: str, timeout_minutes: int = 5
    ):
        self._session_id = str(uuid.uuid4())
        self._card_number = card_number
        self._account_number = account_number
        self._status = SessionStatus.ACTIVE
        self._created_at = datetime.now()
        self._last_activity = self._created_at
        self._timeout_duration = timedelta(minutes=timeout_minutes)
        self._transaction_count = 0
        self._max_transactions_per_session = 10
        self._is_authenticated = False

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def card_number(self) -> str:
        return self._card_number

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def status(self) -> SessionStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def last_activity(self) -> datetime:
        return self._last_activity

    @property
    def transaction_count(self) -> int:
        return self._transaction_count

    @property
    def is_authenticated(self) -> bool:
        return self._is_authenticated

    def is_active(self) -> bool:
        """Check if session is active and not expired"""
        if self._status != SessionStatus.ACTIVE:
            return False

        if self.is_expired():
            self._status = SessionStatus.EXPIRED
            return False

        return True

    def is_expired(self) -> bool:
        """Check if session has expired"""
        return datetime.now() - self._last_activity > self._timeout_duration

    def authenticate(self):
        """Mark session as authenticated"""
        if self.is_active():
            self._is_authenticated = True
            self._update_activity()

    def update_activity(self):
        """Update last activity timestamp"""
        if self.is_active():
            self._last_activity = datetime.now()

    def increment_transaction_count(self):
        """Increment transaction count"""
        if self.is_active():
            self._transaction_count += 1
            self._update_activity()

            # Check transaction limit
            if self._transaction_count >= self._max_transactions_per_session:
                self.terminate("Maximum transactions reached")

    def terminate(self, reason: str = "User terminated"):
        """Terminate session"""
        self._status = SessionStatus.TERMINATED
        self._is_authenticated = False

    def lock(self, reason: str = "Security lock"):
        """Lock session for security reasons"""
        self._status = SessionStatus.LOCKED
        self._is_authenticated = False

    def get_remaining_time_minutes(self) -> float:
        """Get remaining session time in minutes"""
        if not self.is_active():
            return 0

        elapsed = datetime.now() - self._last_activity
        remaining = self._timeout_duration - elapsed

        return max(0, remaining.total_seconds() / 60)

    def get_session_duration_minutes(self) -> float:
        """Get total session duration in minutes"""
        return (datetime.now() - self._created_at).total_seconds() / 60

    def _update_activity(self):
        """Internal method to update activity"""
        self._last_activity = datetime.now()

    def __str__(self) -> str:
        return f"ATMSession({self._session_id[:8]}, {self._status.value}, Auth: {self._is_authenticated})"

    def __repr__(self) -> str:
        return self.__str__()
