"""
Receipt Model
Comprehensive receipt generation with proper formatting
"""

from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, Optional
from dataclasses import dataclass
import uuid


@dataclass
class ReceiptData:
    """Receipt data structure"""

    transaction_id: str
    transaction_type: str
    amount: Optional[Decimal]
    balance_after: Optional[Decimal]
    account_number: str
    card_number: str
    atm_id: str
    location: str
    timestamp: datetime


class Receipt:
    """
    Receipt entity with comprehensive formatting and printing capabilities
    Follows Single Responsibility Principle
    """

    def __init__(self, receipt_data: ReceiptData):
        self._receipt_id = str(uuid.uuid4())
        self._data = receipt_data
        self._generated_at = datetime.now()
        self._is_printed = False

    @property
    def receipt_id(self) -> str:
        return self._receipt_id

    @property
    def data(self) -> ReceiptData:
        return self._data

    @property
    def generated_at(self) -> datetime:
        return self._generated_at

    @property
    def is_printed(self) -> bool:
        return self._is_printed

    def mark_as_printed(self):
        """Mark receipt as printed"""
        self._is_printed = True

    def format_receipt(self) -> str:
        """Format receipt for printing"""
        lines = []
        lines.append("=" * 40)
        lines.append("        ATM TRANSACTION RECEIPT")
        lines.append("=" * 40)
        lines.append("")

        # ATM Information
        lines.append(f"ATM ID: {self._data.atm_id}")
        lines.append(f"Location: {self._data.location}")
        lines.append("")

        # Transaction Information
        lines.append(f"Transaction ID: {self._data.transaction_id}")
        lines.append(f"Transaction Type: {self._data.transaction_type}")
        lines.append(
            f"Date/Time: {self._data.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        lines.append("")

        # Account Information
        masked_account = f"****{self._data.account_number[-4:]}"
        lines.append(f"Account: {masked_account}")

        masked_card = f"****-****-****-{self._data.card_number[-4:]}"
        lines.append(f"Card: {masked_card}")
        lines.append("")

        # Transaction Details
        if self._data.amount is not None:
            lines.append(f"Amount: ${self._data.amount:.2f}")

        if self._data.balance_after is not None:
            lines.append(f"Balance: ${self._data.balance_after:.2f}")

        lines.append("")
        lines.append("Thank you for using our ATM service!")
        lines.append("Please keep this receipt for your records.")
        lines.append("")
        lines.append("=" * 40)

        return "\n".join(lines)

    def format_mini_receipt(self) -> str:
        """Format mini receipt for balance inquiries"""
        lines = []
        lines.append("ATM MINI RECEIPT")
        lines.append("-" * 20)
        lines.append(
            f"Date: {self._data.timestamp.strftime('%Y-%m-%d %H:%M')}"
        )
        lines.append(f"Type: {self._data.transaction_type}")

        if self._data.amount is not None:
            lines.append(f"Amount: ${self._data.amount:.2f}")

        if self._data.balance_after is not None:
            lines.append(f"Balance: ${self._data.balance_after:.2f}")

        lines.append("-" * 20)

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Convert receipt to dictionary for storage/transmission"""
        return {
            "receipt_id": self._receipt_id,
            "transaction_id": self._data.transaction_id,
            "transaction_type": self._data.transaction_type,
            "amount": str(self._data.amount) if self._data.amount else None,
            "balance_after": (
                str(self._data.balance_after)
                if self._data.balance_after
                else None
            ),
            "account_number": self._data.account_number,
            "card_number": self._data.card_number,
            "atm_id": self._data.atm_id,
            "location": self._data.location,
            "timestamp": self._data.timestamp.isoformat(),
            "generated_at": self._generated_at.isoformat(),
            "is_printed": self._is_printed,
        }

    def __str__(self) -> str:
        return (
            f"Receipt({self._receipt_id[:8]}, {self._data.transaction_type})"
        )

    def __repr__(self) -> str:
        return self.__str__()
