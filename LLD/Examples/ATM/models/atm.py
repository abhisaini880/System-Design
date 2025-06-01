"""
ATM Model
Main ATM entity with State pattern and comprehensive functionality
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, Optional, List
import uuid
from abc import ABC, abstractmethod


class ATMStatus(Enum):
    """ATM status enumeration"""

    ACTIVE = "ACTIVE"
    MAINTENANCE = "MAINTENANCE"
    OUT_OF_ORDER = "OUT_OF_ORDER"
    OUT_OF_CASH = "OUT_OF_CASH"
    OFFLINE = "OFFLINE"


class CashDenomination(Enum):
    """Cash denomination enumeration"""

    TWENTY = 20
    FIFTY = 50
    HUNDRED = 100


class ATMState(ABC):
    """Abstract ATM State - State Pattern implementation"""

    @abstractmethod
    def insert_card(self, atm, card) -> bool:
        """Handle card insertion"""
        pass

    @abstractmethod
    def authenticate(self, atm, pin: str) -> bool:
        """Handle PIN authentication"""
        pass

    @abstractmethod
    def select_transaction(self, atm, transaction_type: str) -> bool:
        """Handle transaction selection"""
        pass

    @abstractmethod
    def eject_card(self, atm) -> bool:
        """Handle card ejection"""
        pass

    @abstractmethod
    def get_status_message(self) -> str:
        """Get current state status message"""
        pass


class IdleState(ATMState):
    """ATM Idle State - waiting for card insertion"""

    def insert_card(self, atm, card) -> bool:
        if card and card.is_valid():
            atm._current_card = card
            atm._set_state(atm._card_inserted_state)
            return True
        return False

    def authenticate(self, atm, pin: str) -> bool:
        return False  # Cannot authenticate without card

    def select_transaction(self, atm, transaction_type: str) -> bool:
        return False  # Cannot select transaction in idle state

    def eject_card(self, atm) -> bool:
        return False  # No card to eject

    def get_status_message(self) -> str:
        return "Please insert your card"


class CardInsertedState(ATMState):
    """ATM Card Inserted State - waiting for PIN"""

    def insert_card(self, atm, card) -> bool:
        return False  # Card already inserted

    def authenticate(self, atm, pin: str) -> bool:
        if atm._current_card and atm._current_card.verify_pin(pin):
            # Create session
            atm._create_session()
            atm._set_state(atm._authenticated_state)
            return True
        else:
            # Handle failed authentication
            if atm._current_card and atm._current_card.is_pin_locked:
                atm._eject_card()
                atm._set_state(atm._idle_state)
            return False

    def select_transaction(self, atm, transaction_type: str) -> bool:
        return False  # Must authenticate first

    def eject_card(self, atm) -> bool:
        atm._eject_card()
        atm._set_state(atm._idle_state)
        return True

    def get_status_message(self) -> str:
        return "Please enter your PIN"


class AuthenticatedState(ATMState):
    """ATM Authenticated State - ready for transactions"""

    def insert_card(self, atm, card) -> bool:
        return False  # Card already inserted

    def authenticate(self, atm, pin: str) -> bool:
        return True  # Already authenticated

    def select_transaction(self, atm, transaction_type: str) -> bool:
        atm._set_state(atm._transaction_state)
        return True

    def eject_card(self, atm) -> bool:
        atm._end_session()
        atm._eject_card()
        atm._set_state(atm._idle_state)
        return True

    def get_status_message(self) -> str:
        return "Select transaction type"


class TransactionState(ATMState):
    """ATM Transaction State - processing transaction"""

    def insert_card(self, atm, card) -> bool:
        return False  # Transaction in progress

    def authenticate(self, atm, pin: str) -> bool:
        return True  # Already authenticated

    def select_transaction(self, atm, transaction_type: str) -> bool:
        return False  # Transaction already in progress

    def eject_card(self, atm) -> bool:
        # Complete current transaction first
        atm._set_state(atm._authenticated_state)
        return False

    def get_status_message(self) -> str:
        return "Processing transaction..."


class MaintenanceState(ATMState):
    """ATM Maintenance State - unavailable for service"""

    def insert_card(self, atm, card) -> bool:
        return False

    def authenticate(self, atm, pin: str) -> bool:
        return False

    def select_transaction(self, atm, transaction_type: str) -> bool:
        return False

    def eject_card(self, atm) -> bool:
        return False

    def get_status_message(self) -> str:
        return "ATM temporarily unavailable for maintenance"


class CashManager:
    """Manages ATM cash inventory with denomination tracking"""

    def __init__(self):
        self._cash_inventory: Dict[CashDenomination, int] = {
            CashDenomination.TWENTY: 100,
            CashDenomination.FIFTY: 50,
            CashDenomination.HUNDRED: 30,
        }

    def get_total_cash(self) -> Decimal:
        """Get total cash available"""
        total = Decimal("0")
        for denomination, count in self._cash_inventory.items():
            total += Decimal(str(denomination.value)) * count
        return total

    def can_dispense(self, amount: Decimal) -> bool:
        """Check if amount can be dispensed"""
        if amount <= 0:
            return False

        if amount > self.get_total_cash():
            return False

        # Check if amount can be made with available denominations
        return self._calculate_dispensing(int(amount)) is not None

    def dispense_cash(
        self, amount: Decimal
    ) -> Optional[Dict[CashDenomination, int]]:
        """Dispense cash and return denomination breakdown"""
        if not self.can_dispense(amount):
            return None

        dispensing = self._calculate_dispensing(int(amount))
        if dispensing:
            # Update inventory
            for denomination, count in dispensing.items():
                self._cash_inventory[denomination] -= count

            return dispensing

        return None

    def add_cash(self, denomination: CashDenomination, count: int):
        """Add cash to inventory (refill)"""
        if count > 0:
            self._cash_inventory[denomination] += count

    def get_inventory(self) -> Dict[CashDenomination, int]:
        """Get current cash inventory"""
        return self._cash_inventory.copy()

    def _calculate_dispensing(
        self, amount: int
    ) -> Optional[Dict[CashDenomination, int]]:
        """Calculate optimal denomination breakdown"""
        result = {}
        remaining = amount

        # Use greedy algorithm - start with largest denomination
        for denomination in sorted(
            CashDenomination, key=lambda x: x.value, reverse=True
        ):
            available = self._cash_inventory[denomination]
            needed = min(remaining // denomination.value, available)

            if needed > 0:
                result[denomination] = needed
                remaining -= needed * denomination.value

        return result if remaining == 0 else None


class ATM:
    """
    Main ATM entity implementing State pattern and comprehensive functionality
    Follows SOLID principles and provides complete ATM operations
    """

    def __init__(
        self, atm_id: str, location: str, bank_name: str = "Universal Bank"
    ):
        self._atm_id = atm_id
        self._location = location
        self._bank_name = bank_name
        self._status = ATMStatus.ACTIVE
        self._created_at = datetime.now()
        self._last_maintenance = self._created_at

        # State pattern implementation
        self._idle_state = IdleState()
        self._card_inserted_state = CardInsertedState()
        self._authenticated_state = AuthenticatedState()
        self._transaction_state = TransactionState()
        self._maintenance_state = MaintenanceState()

        self._current_state = self._idle_state

        # Current operation context
        self._current_card = None
        self._current_session = None
        self._current_account = None

        # Cash management
        self._cash_manager = CashManager()

        # Transaction tracking
        self._daily_transaction_count = 0
        self._daily_transaction_amount = Decimal("0")
        self._last_transaction_date = None

        # Maintenance and monitoring
        self._error_log: List[str] = []
        self._transaction_log: List[str] = []

    @property
    def atm_id(self) -> str:
        return self._atm_id

    @property
    def location(self) -> str:
        return self._location

    @property
    def bank_name(self) -> str:
        return self._bank_name

    @property
    def status(self) -> ATMStatus:
        return self._status

    @property
    def current_state_message(self) -> str:
        return self._current_state.get_status_message()

    @property
    def cash_manager(self) -> CashManager:
        return self._cash_manager

    @property
    def current_session(self):
        return self._current_session

    def is_operational(self) -> bool:
        """Check if ATM is operational"""
        return (
            self._status == ATMStatus.ACTIVE
            and self._cash_manager.get_total_cash() > Decimal("100")
        )

    def insert_card(self, card) -> bool:
        """Insert card into ATM"""
        if not self.is_operational():
            return False

        success = self._current_state.insert_card(self, card)
        if success:
            self._log_transaction(f"Card inserted: {card.masked_card_number}")

        return success

    def authenticate_pin(self, pin: str) -> bool:
        """Authenticate with PIN"""
        success = self._current_state.authenticate(self, pin)
        if success:
            self._log_transaction(
                f"Authentication successful for card: {self._current_card.masked_card_number}"
            )
        else:
            self._log_transaction(
                f"Authentication failed for card: {self._current_card.masked_card_number if self._current_card else 'None'}"
            )

        return success

    def select_transaction(self, transaction_type: str) -> bool:
        """Select transaction type"""
        return self._current_state.select_transaction(self, transaction_type)

    def eject_card(self) -> bool:
        """Eject card from ATM"""
        success = self._current_state.eject_card(self)
        if success:
            self._log_transaction("Card ejected")

        return success

    def set_maintenance_mode(self, reason: str = "Scheduled maintenance"):
        """Set ATM to maintenance mode"""
        self._status = ATMStatus.MAINTENANCE
        self._set_state(self._maintenance_state)
        self._log_error(f"Maintenance mode activated: {reason}")

    def exit_maintenance_mode(self):
        """Exit maintenance mode"""
        self._status = ATMStatus.ACTIVE
        self._set_state(self._idle_state)
        self._last_maintenance = datetime.now()
        self._log_transaction("Maintenance mode deactivated")

    def get_daily_stats(self) -> Dict[str, any]:
        """Get daily transaction statistics"""
        return {
            "transaction_count": self._daily_transaction_count,
            "transaction_amount": self._daily_transaction_amount,
            "cash_remaining": self._cash_manager.get_total_cash(),
            "last_transaction_date": self._last_transaction_date,
        }

    def get_error_log(self, limit: int = 50) -> List[str]:
        """Get recent error log entries"""
        return self._error_log[-limit:]

    def get_transaction_log(self, limit: int = 100) -> List[str]:
        """Get recent transaction log entries"""
        return self._transaction_log[-limit:]

    def _set_state(self, new_state: ATMState):
        """Internal method to change ATM state"""
        self._current_state = new_state

    def _create_session(self):
        """Create new ATM session"""
        from .session import ATMSession

        if self._current_card:
            self._current_session = ATMSession(
                card_number=self._current_card.card_number,
                account_number=self._current_card.account_number,
            )
            self._current_session.authenticate()

    def _end_session(self):
        """End current ATM session"""
        if self._current_session:
            self._current_session.terminate("Session ended")
            self._current_session = None

    def _eject_card(self):
        """Internal method to eject card"""
        self._current_card = None
        self._current_account = None
        self._end_session()

    def _log_transaction(self, message: str):
        """Log transaction activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self._transaction_log.append(log_entry)

        # Keep only last 1000 entries
        if len(self._transaction_log) > 1000:
            self._transaction_log = self._transaction_log[-1000:]

    def _log_error(self, message: str):
        """Log error activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] ERROR: {message}"
        self._error_log.append(log_entry)

        # Keep only last 500 entries
        if len(self._error_log) > 500:
            self._error_log = self._error_log[-500:]

    def __str__(self) -> str:
        return f"ATM({self._atm_id}, {self._location}, {self._status.value})"

    def __repr__(self) -> str:
        return self.__str__()
