# 📗 Basic Level LLD Questions (1-5)

## Question 1: Library Management System ⭐
**Difficulty**: Easy | **Time**: 2-3 hours | **Status**: ⏳ Pending

### Problem Statement
Design a Library Management System that allows librarians to manage books, members, and book lending operations.

### Requirements
- **Books**: Title, Author, ISBN, Genre, Availability Status
- **Members**: Name, Member ID, Contact Info, Borrowed Books List
- **Operations**: 
  - Add/Remove books and members
  - Issue/Return books
  - Search books by title, author, or ISBN
  - View member borrowing history
  - Fine calculation for overdue books

### Key Concepts to Practice
- Basic OOP principles
- Enum for book status
- Date handling for due dates
- Simple search algorithms

### Expected Classes
- `Book`, `Member`, `Library`, `Transaction`, `BookStatus` (enum)

---

## Question 2: Vending Machine ⭐
**Difficulty**: Easy | **Time**: 2-3 hours | **Status**: ⏳ Pending

### Problem Statement
Design a vending machine that can dispense products when correct payment is made.

### Requirements
- **Products**: Name, Price, Quantity Available
- **Payment**: Cash, Card support with change calculation
- **Operations**:
  - Select product
  - Insert money/card payment
  - Dispense product and change
  - Restock products
  - Handle insufficient funds/out of stock

### Key Concepts to Practice
- State pattern for machine states
- Strategy pattern for payment methods
- Error handling and edge cases

### Expected Classes
- `Product`, `VendingMachine`, `PaymentMethod`, `CashPayment`, `CardPayment`, `MachineState`

---

## Question 3: Parking Lot System ⭐ ✅
**Difficulty**: Easy | **Time**: 3-4 hours | **Status**: ✅ Completed

### Problem Statement
Already implemented in `/MachineCoding/ParkingLot/` - will be moved to Examples folder.

---

## Question 4: ATM Machine ⭐
**Difficulty**: Easy | **Time**: 3-4 hours | **Status**: 🔄 In Progress

### Problem Statement
Design an ATM system that allows users to perform banking operations.

### Requirements
- **User Operations**: Balance inquiry, Cash withdrawal, Deposit, PIN change
- **Account Types**: Savings, Checking with different withdrawal limits
- **Security**: PIN verification, account locking after failed attempts
- **Cash Management**: ATM cash inventory, denomination handling

### Key Concepts to Practice
- State pattern for ATM states
- Strategy pattern for account types
- Security and validation
- Transaction logging

### Expected Classes
- `ATM`, `Account`, `User`, `Transaction`, `CashDispenser`, `ATMState`

---

## Question 5: Traffic Light System ⭐
**Difficulty**: Easy | **Time**: 2-3 hours | **Status**: ⏳ Pending

### Problem Statement
Design a traffic light control system for a 4-way intersection.

### Requirements
- **Traffic Lights**: Red, Yellow, Green states with timing
- **Intersection**: 4 directions (North, South, East, West)
- **Control Logic**: 
  - Normal operation cycle
  - Emergency vehicle priority
  - Pedestrian crossing requests
  - Rush hour timing adjustments

### Key Concepts to Practice
- State pattern for light states
- Observer pattern for intersection coordination
- Timer-based state transitions
- Priority handling

### Expected Classes
- `TrafficLight`, `Intersection`, `LightState`, `TrafficController`, `EmergencyVehicle`

---

## 🎯 Learning Objectives for Basic Level

### Core OOP Concepts
- [ ] Class design and relationships
- [ ] Encapsulation and data hiding
- [ ] Inheritance hierarchies
- [ ] Polymorphism usage

### Basic Design Patterns
- [ ] Factory Pattern (object creation)
- [ ] Strategy Pattern (algorithm selection)
- [ ] State Pattern (behavior changes)
- [ ] Observer Pattern (notifications)

### Fundamental Skills
- [ ] Requirements analysis
- [ ] Class diagram creation
- [ ] Error handling
- [ ] Code organization
- [ ] Documentation writing

## 📝 Completion Checklist

For each problem, ensure you have:
- [ ] **Problem Analysis**: Break down requirements clearly
- [ ] **Class Design**: Identify entities and their relationships
- [ ] **Implementation**: Write clean, well-documented code
- [ ] **Testing**: Create driver code with test scenarios
- [ ] **Documentation**: README with design decisions
- [ ] **Patterns**: Identify and implement appropriate design patterns

## 🚀 Next Steps
Once you complete all Basic Level questions:
1. Review and refactor your solutions
2. Compare different approaches for the same problem
3. Practice explaining your design decisions
4. Move to Intermediate Level questions

---

*Focus on understanding core OOP principles and basic design patterns. These foundation problems prepare you for more complex system designs.*