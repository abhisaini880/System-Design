# 🏗️ Low-Level Design (LLD) Examples

This folder contains comprehensive Low-Level Design examples that demonstrate object-oriented programming principles, design patterns, and system architecture best practices.

## 📚 Available Examples

### 🏧 [ATM System](./ATM/)
**Complexity**: Intermediate  
**Key Concepts**: State Pattern, Command Pattern, Strategy Pattern  
**Features**: Card authentication, cash withdrawal, balance inquiry, deposit, receipt printing

### 🚗 [Parking Lot System](./ParkingLot/)  
**Complexity**: Intermediate  
**Key Concepts**: Factory Pattern, Observer Pattern, Strategy Pattern  
**Features**: Multi-level parking, different vehicle types, payment processing, spot allocation

### 💰 [Splitwise System](./Splitwise/)
**Complexity**: Advanced  
**Key Concepts**: Strategy Pattern, Factory Pattern, Observer Pattern  
**Features**: Expense splitting, multiple split strategies, group management, payment tracking

## 🎯 Learning Objectives

### Object-Oriented Design Principles
- **Encapsulation**: Data hiding and proper access modifiers
- **Inheritance**: Code reuse through class hierarchies
- **Polymorphism**: Runtime behavior variation
- **Abstraction**: Hiding implementation complexity

### SOLID Principles Implementation
- **S**ingle Responsibility Principle
- **O**pen/Closed Principle  
- **L**iskov Substitution Principle
- **I**nterface Segregation Principle
- **D**ependency Inversion Principle

### Design Patterns Used
- **Creational**: Factory, Builder, Singleton
- **Structural**: Adapter, Facade, Composite
- **Behavioral**: Strategy, Observer, State, Command

## 🏗️ Architecture Standards

### Project Structure
```
SystemName/
├── README.md              # System overview and requirements
├── main.py               # Entry point and demonstration
├── models/               # Core entities and value objects
│   ├── __init__.py
│   ├── entity1.py
│   └── entity2.py
├── services/             # Business logic and use cases
│   ├── __init__.py
│   └── service.py
├── repositories/         # Data access layer
│   ├── __init__.py
│   └── repository.py
├── interfaces/           # Abstract base classes
│   ├── __init__.py
│   └── interface.py
├── enums/               # Enumerations and constants
│   ├── __init__.py
│   └── constants.py
└── exceptions/          # Custom exceptions
    ├── __init__.py
    └── exceptions.py
```

### Code Quality Standards
- **Type Hints**: All methods and functions include type annotations
- **Documentation**: Comprehensive docstrings for all classes and methods
- **Error Handling**: Custom exceptions and proper error propagation
- **Testing**: Unit tests for critical functionality
- **Logging**: Structured logging for debugging and monitoring

## 🚀 Getting Started

### Prerequisites
```bash
python 3.8+
```

### Running Examples
```bash
# ATM System
cd ATM/python && python main.py

# Parking Lot System  
cd ParkingLot && python main.py

# Splitwise System
cd Splitwise/python && python main.py
```

## 📖 Study Guide

### For Beginners
1. Start with **ATM System** - demonstrates basic state management
2. Focus on understanding class relationships and inheritance
3. Study the use of enums and constants

### For Intermediate
1. Move to **Parking Lot System** - complex object relationships
2. Understand factory patterns and strategy implementations
3. Learn about observer pattern for real-time updates

### For Advanced
1. Tackle **Splitwise System** - most complex business logic
2. Master multiple design patterns working together
3. Understand advanced architectural concepts

## 🔍 Interview Preparation

### Common LLD Interview Questions
1. **Design an ATM System** - State management, security, concurrency
2. **Design a Parking Lot** - Spatial optimization, pricing strategies
3. **Design a Bill Splitting App** - Complex algorithms, financial calculations

### Key Discussion Points
- **Scalability**: How would you scale these systems?
- **Concurrency**: How to handle multiple users?
- **Security**: What security measures are needed?
- **Performance**: Optimization strategies for large-scale usage

## 💡 Best Practices Demonstrated

### Design Principles
- **Favor composition over inheritance**
- **Program to interfaces, not implementations**
- **Minimize coupling between components**
- **Maximize cohesion within components**

### Code Organization
- **Clean separation of concerns**
- **Consistent naming conventions**
- **Proper error handling and validation**
- **Comprehensive logging and monitoring**

## 🛠️ Extension Ideas

### ATM System Extensions
- Multi-bank support
- Cryptocurrency transactions
- Mobile app integration
- Fraud detection

### Parking Lot Extensions
- Reservation system
- Electric vehicle charging
- Valet parking service
- Mobile payment integration

### Splitwise Extensions
- Currency conversion
- Recurring expenses
- Tax calculation
- Integration with payment gateways

---

## ✅ Validation Checklist

Before considering an LLD complete, ensure:
- [ ] All SOLID principles are followed
- [ ] Appropriate design patterns are used
- [ ] Code is well-documented and tested
- [ ] Error handling is comprehensive
- [ ] The system is extensible and maintainable
- [ ] Performance considerations are addressed

**Next Steps**: Choose a system based on your current skill level and start implementing!