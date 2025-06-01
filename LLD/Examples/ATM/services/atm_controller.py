"""
ATM Controller
Main controller implementing Facade pattern and coordinating all ATM operations
"""

from decimal import Decimal
from typing import Optional, Dict, Any
from datetime import datetime

from models import (
    ATM,
    Card,
    Account,
    Transaction,
    TransactionResult,
    Receipt,
    ReceiptData,
)
from enums.constants import TransactionType
from exceptions.atm_exceptions import *
from .authentication_service import AuthenticationService
from .transaction_service import TransactionService
from .receipt_service import ReceiptService
from .account_service import AccountService


class ATMController:
    """
    Main ATM Controller implementing Facade pattern
    Coordinates all ATM operations and services
    Follows SOLID principles and provides clean API
    """

    def __init__(
        self,
        atm: ATM,
        account_service: AccountService,
        authentication_service: Optional[AuthenticationService] = None,
        transaction_service: Optional[TransactionService] = None,
        receipt_service: Optional[ReceiptService] = None,
    ):
        self._atm = atm
        self._account_service = account_service

        # Dependency injection with default implementations
        self._auth_service = authentication_service or AuthenticationService()
        self._transaction_service = transaction_service or TransactionService(
            atm.cash_manager
        )
        self._receipt_service = receipt_service or ReceiptService()

        self._current_account: Optional[Account] = None

    @property
    def atm(self) -> ATM:
        return self._atm

    @property
    def current_account(self) -> Optional[Account]:
        return self._current_account

    @property
    def current_session(self):
        return self._atm.current_session

    def insert_card(self, card: Card) -> bool:
        """
        Insert card into ATM
        Returns True if card is successfully inserted and valid
        """
        try:
            if not self._atm.is_operational():
                raise MaintenanceModeException()

            if not card:
                raise CardReaderException("No card provided")

            # Validate card
            if card.is_expired():
                raise CardExpiredException(card.expiry_date)

            if not card.is_valid():
                raise CardBlockedException(
                    "Card is not valid for transactions"
                )

            # Insert card into ATM
            success = self._atm.insert_card(card)
            if success:
                # Load associated account
                self._current_account = (
                    self._account_service.get_account_by_number(
                        card.account_number
                    )
                )
                if not self._current_account:
                    self._atm.eject_card()
                    raise AuthenticationException(
                        "Account not found", ErrorCode.ACCOUNT_NOT_FOUND
                    )

            return success

        except ATMException:
            raise
        except Exception as e:
            raise ATMException(
                f"Card insertion failed: {str(e)}", ErrorCode.SYSTEM_ERROR
            )

    def authenticate_pin(self, pin: str) -> bool:
        """
        Authenticate user with PIN
        Returns True if authentication successful
        """
        try:
            if not self._atm._current_card:
                raise AuthenticationException(
                    "No card inserted", ErrorCode.NO_CARD
                )

            # Validate PIN format
            if not self._auth_service.validate_pin_format(pin):
                raise InvalidPINException(
                    self._atm._current_card.failed_attempts
                )

            # Authenticate PIN
            success = self._atm.authenticate_pin(pin)
            if not success:
                attempts_remaining = (
                    3 - self._atm._current_card.failed_attempts
                )
                if attempts_remaining <= 0:
                    raise CardBlockedException(
                        "Card blocked due to too many failed attempts"
                    )
                else:
                    raise InvalidPINException(attempts_remaining)

            return success

        except ATMException:
            raise
        except Exception as e:
            raise AuthenticationException(
                f"Authentication failed: {str(e)}", ErrorCode.SYSTEM_ERROR
            )

    def withdraw_cash(self, amount: Decimal) -> TransactionResult:
        """
        Withdraw cash from account
        Returns TransactionResult with operation details
        """
        try:
            self._validate_authenticated_session()

            # Validate amount
            if amount <= 0:
                raise InvalidAmountException(
                    amount, Decimal("20"), Decimal("1000")
                )

            if amount % 20 != 0:  # ATM only dispenses $20 denominations
                raise InvalidAmountException(
                    amount, Decimal("20"), Decimal("1000")
                )

            # Create transaction
            transaction = Transaction(
                transaction_type=TransactionType.WITHDRAWAL,
                account_number=self._current_account.account_number,
                amount=amount,
                description=f"ATM Withdrawal at {self._atm.location}",
            )

            # Execute transaction
            result = self._transaction_service.execute_withdrawal(
                transaction, self._current_account, self._atm.cash_manager
            )

            # Generate receipt if successful
            if result.success:
                receipt = self._generate_receipt(transaction, result)
                result.receipt_data = receipt.to_dict()

                # Update session
                if self._atm.current_session:
                    self._atm.current_session.increment_transaction_count()

            return result

        except ATMException:
            raise
        except Exception as e:
            raise TransactionException(
                f"Withdrawal failed: {str(e)}", ErrorCode.SYSTEM_ERROR
            )

    def deposit_cash(self, amount: Decimal) -> TransactionResult:
        """
        Deposit cash to account
        Returns TransactionResult with operation details
        """
        try:
            self._validate_authenticated_session()

            # Validate amount
            if amount <= 0:
                raise InvalidAmountException(
                    amount, Decimal("1"), Decimal("10000")
                )

            # Create transaction
            transaction = Transaction(
                transaction_type=TransactionType.DEPOSIT,
                account_number=self._current_account.account_number,
                amount=amount,
                description=f"ATM Deposit at {self._atm.location}",
            )

            # Execute transaction
            result = self._transaction_service.execute_deposit(
                transaction, self._current_account
            )

            # Generate receipt if successful
            if result.success:
                receipt = self._generate_receipt(transaction, result)
                result.receipt_data = receipt.to_dict()

                # Update session
                if self._atm.current_session:
                    self._atm.current_session.increment_transaction_count()

            return result

        except ATMException:
            raise
        except Exception as e:
            raise TransactionException(
                f"Deposit failed: {str(e)}", ErrorCode.SYSTEM_ERROR
            )

    def check_balance(self) -> TransactionResult:
        """
        Check account balance
        Returns TransactionResult with balance information
        """
        try:
            self._validate_authenticated_session()

            # Create transaction
            transaction = Transaction(
                transaction_type=TransactionType.BALANCE_INQUIRY,
                account_number=self._current_account.account_number,
                description=f"Balance Inquiry at {self._atm.location}",
            )

            # Execute transaction
            result = self._transaction_service.execute_balance_inquiry(
                transaction, self._current_account
            )

            # Generate receipt if successful
            if result.success:
                receipt = self._generate_receipt(transaction, result)
                result.receipt_data = receipt.to_dict()

                # Update session
                if self._atm.current_session:
                    self._atm.current_session.increment_transaction_count()

            return result

        except ATMException:
            raise
        except Exception as e:
            raise TransactionException(
                f"Balance inquiry failed: {str(e)}", ErrorCode.SYSTEM_ERROR
            )

    def transfer_funds(
        self, to_account: str, amount: Decimal
    ) -> TransactionResult:
        """
        Transfer funds to another account
        Returns TransactionResult with transfer details
        """
        try:
            self._validate_authenticated_session()

            # Validate amount
            if amount <= 0:
                raise InvalidAmountException(
                    amount, Decimal("1"), Decimal("10000")
                )

            # Validate target account
            target_account = self._account_service.get_account_by_number(
                to_account
            )
            if not target_account:
                raise TransactionException(
                    "Target account not found", ErrorCode.ACCOUNT_NOT_FOUND
                )

            # Create transaction
            transaction = Transaction(
                transaction_type=TransactionType.TRANSFER,
                account_number=self._current_account.account_number,
                amount=amount,
                description=f"Transfer to {to_account} at {self._atm.location}",
            )
            transaction.add_metadata("target_account", to_account)

            # Execute transfer
            result = self._transaction_service.execute_transfer(
                transaction, self._current_account, target_account
            )

            # Generate receipt if successful
            if result.success:
                receipt = self._generate_receipt(transaction, result)
                result.receipt_data = receipt.to_dict()

                # Update session
                if self._atm.current_session:
                    self._atm.current_session.increment_transaction_count()

            return result

        except ATMException:
            raise
        except Exception as e:
            raise TransactionException(
                f"Transfer failed: {str(e)}", ErrorCode.SYSTEM_ERROR
            )

    def change_pin(self, old_pin: str, new_pin: str) -> TransactionResult:
        """
        Change card PIN
        Returns TransactionResult with operation status
        """
        try:
            self._validate_authenticated_session()

            # Validate new PIN
            if not self._auth_service.validate_pin_format(new_pin):
                raise InvalidPINException(0)

            # Change PIN
            success = self._atm._current_card.change_pin(old_pin, new_pin)
            if not success:
                raise InvalidPINException(
                    self._atm._current_card.failed_attempts
                )

            # Create transaction record
            transaction = Transaction(
                transaction_type=TransactionType.PIN_CHANGE,
                account_number=self._current_account.account_number,
                description=f"PIN Change at {self._atm.location}",
            )
            transaction.complete_successfully()

            return TransactionResult(
                success=True,
                transaction_id=transaction.transaction_id,
                message="PIN changed successfully",
            )

        except ATMException:
            raise
        except Exception as e:
            raise TransactionException(
                f"PIN change failed: {str(e)}", ErrorCode.SYSTEM_ERROR
            )

    def print_receipt(self, transaction_id: str) -> bool:
        """
        Print receipt for transaction
        Returns True if receipt printed successfully
        """
        try:
            # This would interface with actual printer hardware
            # For now, we'll just return True
            return True

        except Exception as e:
            raise HardwareException(f"Receipt printing failed: {str(e)}")

    def eject_card(self) -> bool:
        """
        Eject card and end session
        Returns True if card ejected successfully
        """
        try:
            success = self._atm.eject_card()
            if success:
                self._current_account = None
            return success

        except Exception as e:
            raise HardwareException(f"Card ejection failed: {str(e)}")

    def get_atm_status(self) -> Dict[str, Any]:
        """
        Get current ATM status and information
        """
        return {
            "atm_id": self._atm.atm_id,
            "location": self._atm.location,
            "status": self._atm.status.value,
            "current_state": self._atm.current_state_message,
            "cash_available": str(self._atm.cash_manager.get_total_cash()),
            "is_operational": self._atm.is_operational(),
            "daily_stats": self._atm.get_daily_stats(),
        }

    def get_session_info(self) -> Optional[Dict[str, Any]]:
        """
        Get current session information
        """
        if not self._atm.current_session:
            return None

        session = self._atm.current_session
        return {
            "session_id": session.session_id,
            "status": session.status.value,
            "remaining_time_minutes": session.get_remaining_time_minutes(),
            "transaction_count": session.transaction_count,
            "is_authenticated": session.is_authenticated,
        }

    def _validate_authenticated_session(self):
        """Validate that user is authenticated and session is active"""
        if not self._atm.current_session:
            raise AuthenticationException(
                "No active session", ErrorCode.NO_SESSION
            )

        if not self._atm.current_session.is_authenticated:
            raise AuthenticationException(
                "Session not authenticated", ErrorCode.NOT_AUTHENTICATED
            )

        if not self._atm.current_session.is_active():
            raise AuthenticationException(
                "Session expired", ErrorCode.SESSION_EXPIRED
            )

        if not self._current_account:
            raise AuthenticationException(
                "No account loaded", ErrorCode.ACCOUNT_NOT_FOUND
            )

    def _generate_receipt(
        self, transaction: Transaction, result: TransactionResult
    ) -> Receipt:
        """Generate receipt for transaction"""
        receipt_data = ReceiptData(
            transaction_id=transaction.transaction_id,
            transaction_type=transaction.transaction_type.value,
            amount=transaction.amount if transaction.amount > 0 else None,
            balance_after=result.balance_after,
            account_number=self._current_account.account_number,
            card_number=self._atm._current_card.card_number,
            atm_id=self._atm.atm_id,
            location=self._atm.location,
            timestamp=transaction.created_at,
        )

        return Receipt(receipt_data)

    def __str__(self) -> str:
        return f"ATMController({self._atm.atm_id}, {self._atm.status.value})"

    def __repr__(self) -> str:
        return self.__str__()
