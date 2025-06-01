# 🏧 ATM System - Low Level Design

## 📋 Problem Statement

Design an ATM (Automated Teller Machine) system that allows users to perform banking operations like cash withdrawal, balance inquiry, deposit, and transfer funds with proper authentication and security.

## 🎯 Requirements

### Functional Requirements
1. **Card Authentication**: PIN verification and card validation
2. **Cash Withdrawal**: Withdraw money with balance and limit checks
3. **Balance Inquiry**: Check current account balance
4. **Cash Deposit**: Deposit money to account
5. **Fund Transfer**: Transfer money between accounts
6. **Receipt Printing**: Generate transaction receipts
7. **Transaction History**: View recent transactions

### Non-Functional Requirements
1. **Security**: Secure PIN handling and transaction processing
2. **Reliability**: Handle hardware failures gracefully
3. **Performance**: Quick response times for operations
4. **Concurrency**: Support multiple concurrent users
5. **Audit Trail**: Log all transactions for compliance

## 🏗️ System Architecture

### Design Patterns Used
- **State Pattern**: ATM operational states (idle, authenticated, processing)
- **Command Pattern**: Encapsulate transaction operations
- **Strategy Pattern**: Different transaction types and fee calculations
- **Factory Pattern**: Create different types of transactions
- **Observer Pattern**: Notify about transaction events

### Class Diagram Overview
```
ATMController
├── ATMState (State Pattern)
│   ├── IdleState
│   ├── AuthenticatedState
│   └── TransactionState
├── TransactionService
│   ├── WithdrawalTransaction (Command Pattern)
│   ├── DepositTransaction
│   ├── BalanceInquiryTransaction
│   └── TransferTransaction
├── AuthenticationService
├── CardReader
├── CashDispenser
└── ReceiptPrinter
```

## 🔧 Key Components

### 1. ATM States
- **Idle**: Waiting for card insertion
- **Authenticated**: PIN verified, ready for transactions
- **Transaction**: Processing current transaction
- **Maintenance**: ATM under maintenance

### 2. Transaction Types
- **Withdrawal**: Cash withdrawal with balance checks
- **Deposit**: Cash/check deposit processing
- **Balance Inquiry**: Account balance retrieval
- **Transfer**: Inter-account fund transfers

### 3. Hardware Components
- **Card Reader**: Read and validate cards
- **PIN Pad**: Secure PIN entry
- **Cash Dispenser**: Dispense cash safely
- **Deposit Slot**: Accept cash/check deposits
- **Receipt Printer**: Print transaction receipts

## 🚀 Usage Example

```python
# Initialize ATM
atm = ATMController("ATM_001", "Downtown Branch")

# Insert card
card = Card("1234567890123456", "12/25", "123")
atm.insert_card(card)

# Enter PIN
if atm.authenticate("1234"):
    # Perform withdrawal
    result = atm.withdraw(Decimal("100.00"))
    
    # Print receipt
    if result.success:
        atm.print_receipt(result.transaction_id)
        
# Remove card
atm.eject_card()
```

## 📁 Project Structure

```
ATM/
├── README.md
├── main.py
├── models/
│   ├── __init__.py
│   ├── account.py
│   ├── card.py
│   ├── transaction.py
│   └── atm.py
├── services/
│   ├── __init__.py
│   ├── atm_service.py
│   ├── auth_service.py
│   ├── transaction_service.py
│   └── hardware_service.py
├── interfaces/
│   ├── __init__.py
│   ├── atm_state.py
│   ├── transaction_handler.py
│   └── hardware_interface.py
├── enums/
│   ├── __init__.py
│   └── constants.py
└── exceptions/
    ├── __init__.py
    └── atm_exceptions.py
```

## 🔒 Security Features

1. **PIN Encryption**: Secure PIN storage and transmission
2. **Transaction Limits**: Daily withdrawal and transfer limits
3. **Session Timeout**: Automatic logout after inactivity
4. **Audit Logging**: Complete transaction audit trail
5. **Card Retention**: Retain suspicious cards

## 🎨 Extension Points

1. **Multi-Bank Support**: Support cards from different banks
2. **Biometric Authentication**: Fingerprint/facial recognition
3. **Mobile Integration**: QR code transactions
4. **Cryptocurrency**: Bitcoin/altcoin transactions
5. **AI Fraud Detection**: Machine learning fraud prevention

---

**Implementation Details**: See individual Python files for complete implementation with type hints, error handling, and comprehensive documentation.