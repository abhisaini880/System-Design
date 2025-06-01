#!/usr/bin/env python3
"""
ATM System Demonstration
"""

from datetime import date
from decimal import Decimal

from models import Account, Card, ATM, AccountType
from enums.constants import TransactionType
from exceptions.atm_exceptions import (
    InsufficientFundsException,
    InvalidPINException,
    CardBlockedException,
)
from services.atm_controller import ATMController


def create_sample_data():
    """Create sample accounts and cards for demonstration"""

    # Create sample accounts
    account1 = Account(
        account_number="ACC001",
        account_holder_name="John Doe",
        account_type=AccountType.SAVINGS,
        balance=Decimal("5000.00"),
    )

    account2 = Account(
        account_number="ACC002",
        account_holder_name="Jane Smith",
        account_type=AccountType.CHECKING,
        balance=Decimal("3000.00"),
    )

    account3 = Account(
        account_number="ACC003",
        account_holder_name="Bob Johnson",
        account_type=AccountType.SAVINGS,
        balance=Decimal("100.00"),  # Low balance for testing
    )

    # Create sample cards
    card1 = Card(
        card_number="1234567890123456",
        pin="1234",
        account=account1,
        expiry_date="2027-12-31",
        is_blocked=False,
    )

    card2 = Card(
        card_number="9876543210987654",
        pin="5678",
        account=account2,
        expiry_date="2026-08-15",
        is_blocked=False,
    )

    card3 = Card(
        card_number="5555666677778888",
        pin="9999",
        account=account3,
        expiry_date="2025-03-31",
        is_blocked=True,  # Blocked card for testing
    )

    return [card1, card2, card3]


def demonstrate_successful_transactions():
    """Demonstrate successful ATM transactions"""
    print("=== Successful Transactions Demo ===")

    # Create ATM and controller
    atm = ATM(
        atm_id="ATM001",
        location="Main Street Branch",
        cash_available=Decimal("50000.00"),
    )

    controller = ATMController(atm)
    cards = create_sample_data()

    # Register cards with the controller
    for card in cards:
        controller._cards[card.card_number] = card

    try:
        # Test 1: Successful balance inquiry
        print("\n--- Test 1: Balance Inquiry ---")
        session = controller.insert_card("1234567890123456")
        if controller.authenticate("1234"):
            result = controller.check_balance()
            print(f"Balance inquiry successful: {result}")
            controller.end_session()

        # Test 2: Successful withdrawal
        print("\n--- Test 2: Cash Withdrawal ---")
        session = controller.insert_card("1234567890123456")
        if controller.authenticate("1234"):
            result = controller.withdraw_cash(Decimal("500.00"))
            print(f"Withdrawal successful: {result}")
            controller.end_session()

        # Test 3: Successful deposit
        print("\n--- Test 3: Cash Deposit ---")
        session = controller.insert_card("9876543210987654")
        if controller.authenticate("5678"):
            result = controller.deposit_cash(Decimal("1000.00"))
            print(f"Deposit successful: {result}")
            controller.end_session()

    except Exception as e:
        print(f"Unexpected error: {e}")


def demonstrate_error_scenarios():
    """Demonstrate various error scenarios"""
    print("\n=== Error Scenarios Demo ===")

    atm = ATM(
        atm_id="ATM002",
        location="Downtown Branch",
        cash_available=Decimal("1000.00"),  # Low cash for testing
    )

    controller = ATMController(atm)
    cards = create_sample_data()

    # Register cards
    for card in cards:
        controller._cards[card.card_number] = card

    # Test 1: Invalid card
    print("\n--- Test 1: Invalid Card ---")
    try:
        session = controller.insert_card("0000000000000000")
        print("This should not be reached")
    except Exception as e:
        print(f"Expected error: {e}")

    # Test 2: Invalid PIN
    print("\n--- Test 2: Invalid PIN ---")
    try:
        session = controller.insert_card("1234567890123456")
        if not controller.authenticate("0000"):
            print("Authentication failed as expected")
        else:
            controller.end_session()
    except InvalidPINException as e:
        print(f"Expected error: {e}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 3: Blocked card
    print("\n--- Test 3: Blocked Card ---")
    try:
        session = controller.insert_card("5555666677778888")
        if controller.authenticate("9999"):
            print("This should not be reached")
        controller.end_session()
    except CardBlockedException as e:
        print(f"Expected error: {e}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 4: Insufficient funds
    print("\n--- Test 4: Insufficient Funds ---")
    try:
        session = controller.insert_card("5555666677778888")
        # First unblock the card for this test
        controller._cards["5555666677778888"].is_blocked = False
        if controller.authenticate("9999"):
            result = controller.withdraw_cash(
                Decimal("1000.00")
            )  # More than account balance
            print("This should not be reached")
        controller.end_session()
    except InsufficientFundsException as e:
        print(f"Expected error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def demonstrate_transaction_history():
    """Demonstrate transaction history and receipt generation"""
    print("\n=== Transaction History Demo ===")

    atm = ATM(
        atm_id="ATM003",
        location="Airport Branch",
        cash_available=Decimal("25000.00"),
    )

    controller = ATMController(atm)
    cards = create_sample_data()

    # Register cards
    for card in cards:
        controller._cards[card.card_number] = card

    try:
        # Perform multiple transactions
        session = controller.insert_card("1234567890123456")
        if controller.authenticate("1234"):
            # Multiple operations
            controller.check_balance()
            controller.withdraw_cash(Decimal("200.00"))
            controller.deposit_cash(Decimal("100.00"))
            controller.check_balance()

            # Print transaction history
            history = session.get_transaction_history()
            print(f"\nTransaction History ({len(history)} transactions):")
            for i, transaction in enumerate(history, 1):
                print(
                    f"{i}. {transaction.transaction_type.value}: "
                    f"${transaction.amount} at {transaction.timestamp}"
                )

            controller.end_session()

    except Exception as e:
        print(f"Error in transaction history demo: {e}")


def main():
    """Main demonstration function"""
    print("ATM System Demonstration")
    print("=" * 50)

    try:
        demonstrate_successful_transactions()
        demonstrate_error_scenarios()
        demonstrate_transaction_history()

        print("\n" + "=" * 50)
        print("ATM System demonstration completed successfully!")

    except Exception as e:
        print(f"Critical error in demonstration: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
