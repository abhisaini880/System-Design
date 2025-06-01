"""
Receipt Service
Handles receipt generation, formatting, and printing operations
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from models import Receipt, ReceiptData, Transaction


class ReceiptService:
    """
    Receipt service implementing Strategy pattern for different receipt formats
    Handles receipt generation, formatting, and management
    """

    def __init__(self):
        self._receipt_storage: Dict[str, Receipt] = {}
        self._print_queue: List[str] = []  # Receipt IDs waiting to be printed

    def generate_receipt(self, receipt_data: ReceiptData) -> Receipt:
        """
        Generate a receipt from transaction data
        """
        receipt = Receipt(receipt_data)
        self._receipt_storage[receipt.receipt_id] = receipt
        return receipt

    def format_transaction_receipt(self, receipt: Receipt) -> str:
        """
        Format full transaction receipt
        """
        return receipt.format_receipt()

    def format_mini_receipt(self, receipt: Receipt) -> str:
        """
        Format mini receipt for balance inquiries
        """
        return receipt.format_mini_receipt()

    def queue_for_printing(self, receipt_id: str) -> bool:
        """
        Add receipt to print queue
        """
        if receipt_id in self._receipt_storage:
            if receipt_id not in self._print_queue:
                self._print_queue.append(receipt_id)
            return True
        return False

    def print_next_receipt(self) -> Optional[str]:
        """
        Print next receipt in queue
        Returns formatted receipt string or None if queue is empty
        """
        if not self._print_queue:
            return None

        receipt_id = self._print_queue.pop(0)
        receipt = self._receipt_storage.get(receipt_id)

        if receipt:
            receipt.mark_as_printed()
            return self.format_transaction_receipt(receipt)

        return None

    def get_receipt(self, receipt_id: str) -> Optional[Receipt]:
        """
        Get receipt by ID
        """
        return self._receipt_storage.get(receipt_id)

    def get_receipt_history(
        self, account_number: str, limit: int = 10
    ) -> List[Receipt]:
        """
        Get receipt history for an account
        """
        receipts = [
            receipt
            for receipt in self._receipt_storage.values()
            if receipt.data.account_number == account_number
        ]

        # Sort by timestamp (newest first)
        receipts.sort(key=lambda r: r.data.timestamp, reverse=True)

        return receipts[:limit]

    def generate_daily_summary_receipt(
        self, atm_id: str, location: str, transactions: List[Transaction]
    ) -> str:
        """
        Generate daily summary receipt for ATM operations
        """
        lines = []
        lines.append("=" * 50)
        lines.append("         ATM DAILY SUMMARY REPORT")
        lines.append("=" * 50)
        lines.append("")

        lines.append(f"ATM ID: {atm_id}")
        lines.append(f"Location: {location}")
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append(
            f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        lines.append("")

        # Transaction summary
        total_transactions = len(transactions)
        successful_transactions = len(
            [t for t in transactions if t.is_completed()]
        )
        failed_transactions = len([t for t in transactions if t.is_failed()])

        lines.append("TRANSACTION SUMMARY:")
        lines.append(f"Total Transactions: {total_transactions}")
        lines.append(f"Successful: {successful_transactions}")
        lines.append(f"Failed: {failed_transactions}")
        lines.append("")

        # Transaction type breakdown
        type_counts = {}
        for transaction in transactions:
            t_type = transaction.transaction_type.value
            type_counts[t_type] = type_counts.get(t_type, 0) + 1

        lines.append("TRANSACTION TYPES:")
        for t_type, count in type_counts.items():
            lines.append(f"{t_type}: {count}")
        lines.append("")

        # Amount summary (for withdrawal/deposit transactions)
        withdrawal_total = sum(
            t.amount
            for t in transactions
            if t.transaction_type.value == "WITHDRAWAL" and t.is_completed()
        )
        deposit_total = sum(
            t.amount
            for t in transactions
            if t.transaction_type.value == "DEPOSIT" and t.is_completed()
        )

        lines.append("AMOUNT SUMMARY:")
        lines.append(f"Total Withdrawals: ${withdrawal_total:.2f}")
        lines.append(f"Total Deposits: ${deposit_total:.2f}")
        lines.append(
            f"Net Cash Flow: ${deposit_total - withdrawal_total:.2f}"
        )
        lines.append("")

        lines.append("=" * 50)
        lines.append("End of Report")
        lines.append("=" * 50)

        return "\n".join(lines)

    def export_receipts_to_csv(self, account_number: str) -> str:
        """
        Export receipts for an account to CSV format
        """
        receipts = self.get_receipt_history(account_number, limit=1000)

        csv_lines = []
        csv_lines.append(
            "Receipt ID,Transaction ID,Type,Amount,Balance,Date,ATM ID,Location"
        )

        for receipt in receipts:
            data = receipt.data
            csv_lines.append(
                f"{receipt.receipt_id},"
                f"{data.transaction_id},"
                f"{data.transaction_type},"
                f"{data.amount or ''},"
                f"{data.balance_after or ''},"
                f"{data.timestamp.isoformat()},"
                f"{data.atm_id},"
                f'"{data.location}"'
            )

        return "\n".join(csv_lines)

    def clear_old_receipts(self, days_to_keep: int = 90):
        """
        Clear receipts older than specified days
        """
        cutoff_date = datetime.now().timestamp() - (
            days_to_keep * 24 * 60 * 60
        )

        receipts_to_remove = [
            receipt_id
            for receipt_id, receipt in self._receipt_storage.items()
            if receipt.generated_at.timestamp() < cutoff_date
        ]

        for receipt_id in receipts_to_remove:
            del self._receipt_storage[receipt_id]

            # Remove from print queue if present
            if receipt_id in self._print_queue:
                self._print_queue.remove(receipt_id)

        return len(receipts_to_remove)

    def get_print_queue_status(self) -> Dict[str, Any]:
        """
        Get current print queue status
        """
        return {
            "queue_length": len(self._print_queue),
            "pending_receipts": self._print_queue.copy(),
            "total_receipts": len(self._receipt_storage),
        }
