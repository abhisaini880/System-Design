"""
Account Service
Handles account management and operations
"""

from typing import Optional, Dict, List
from decimal import Decimal
from models import Account, AccountType, AccountLimits


class AccountService:
    """
    Account service for managing account operations
    Acts as a repository pattern implementation
    """

    def __init__(self):
        # In-memory storage for demonstration
        # In production, this would connect to a database
        self._accounts: Dict[str, Account] = {}
        self._accounts_by_card: Dict[str, str] = (
            {}
        )  # card_number -> account_number

    def create_account(
        self,
        account_number: str,
        account_type: AccountType,
        holder_name: str,
        initial_balance: Decimal = Decimal("0"),
        limits: Optional[AccountLimits] = None,
    ) -> Account:
        """
        Create a new account
        """
        if account_number in self._accounts:
            raise ValueError(f"Account {account_number} already exists")

        account = Account(
            account_number=account_number,
            account_type=account_type,
            holder_name=holder_name,
            initial_balance=initial_balance,
            limits=limits,
        )

        self._accounts[account_number] = account
        return account

    def get_account_by_number(self, account_number: str) -> Optional[Account]:
        """
        Get account by account number
        """
        return self._accounts.get(account_number)

    def get_account_by_card(self, card_number: str) -> Optional[Account]:
        """
        Get account associated with card number
        """
        account_number = self._accounts_by_card.get(card_number)
        if account_number:
            return self._accounts.get(account_number)
        return None

    def link_card_to_account(self, card_number: str, account_number: str):
        """
        Link a card to an account
        """
        if account_number not in self._accounts:
            raise ValueError(f"Account {account_number} does not exist")

        self._accounts_by_card[card_number] = account_number

    def update_account_balance(
        self, account_number: str, new_balance: Decimal
    ) -> bool:
        """
        Update account balance (for external transactions)
        """
        account = self._accounts.get(account_number)
        if account:
            # This is a simplified update - in production would have proper transaction handling
            account._balance = new_balance
            return True
        return False

    def freeze_account(
        self, account_number: str, reason: str = "Security freeze"
    ) -> bool:
        """
        Freeze account for security reasons
        """
        account = self._accounts.get(account_number)
        if account:
            account.freeze_account(reason)
            return True
        return False

    def unfreeze_account(self, account_number: str) -> bool:
        """
        Unfreeze account
        """
        account = self._accounts.get(account_number)
        if account:
            account.unfreeze_account()
            return True
        return False

    def get_account_transaction_history(
        self, account_number: str, limit: int = 10
    ) -> List[str]:
        """
        Get account transaction history
        """
        account = self._accounts.get(account_number)
        if account:
            return account.get_transaction_history(limit)
        return []

    def validate_account_for_transaction(
        self, account_number: str, amount: Decimal, transaction_type: str
    ) -> bool:
        """
        Validate if account can perform transaction
        """
        account = self._accounts.get(account_number)
        if not account:
            return False

        if not account.is_active():
            return False

        if transaction_type.upper() == "WITHDRAWAL":
            return account.can_withdraw(amount)
        elif transaction_type.upper() == "DEPOSIT":
            return account.can_deposit(amount)

        return True

    def get_all_accounts(self) -> List[Account]:
        """
        Get all accounts (admin function)
        """
        return list(self._accounts.values())

    def delete_account(self, account_number: str) -> bool:
        """
        Delete account (admin function)
        """
        if account_number in self._accounts:
            # Remove account
            del self._accounts[account_number]

            # Remove card associations
            cards_to_remove = [
                card
                for card, acc in self._accounts_by_card.items()
                if acc == account_number
            ]
            for card in cards_to_remove:
                del self._accounts_by_card[card]

            return True
        return False
