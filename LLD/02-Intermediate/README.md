# 📘 Intermediate Level LLD Questions (6-10)

## Question 6: Online Shopping Cart ⭐⭐
**Difficulty**: Medium | **Time**: 4-5 hours | **Status**: ⏳ Pending

### Problem Statement
Design an e-commerce shopping cart system with product catalog, inventory management, and order processing.

### Requirements
- **Products**: Categories, variants (size, color), pricing, inventory
- **Cart Operations**: Add/remove items, quantity updates, price calculation
- **Discounts**: Percentage, fixed amount, buy-X-get-Y, category-based
- **Orders**: Checkout process, order history, status tracking
- **Inventory**: Stock management, low-stock alerts

### Key Concepts to Practice
- Composite pattern for product categories
- Strategy pattern for discount calculations
- Observer pattern for inventory updates
- Command pattern for cart operations

### Expected Classes
- `Product`, `CartItem`, `ShoppingCart`, `DiscountStrategy`, `Order`, `InventoryManager`

---

## Question 7: Hotel Booking System ⭐⭐
**Difficulty**: Medium | **Time**: 4-5 hours | **Status**: ⏳ Pending

### Problem Statement
Design a hotel reservation system with room management, booking operations, and customer management.

### Requirements
- **Rooms**: Types (single, double, suite), amenities, pricing
- **Bookings**: Date range validation, conflicts checking, modifications
- **Customers**: Guest information, booking history, loyalty points
- **Pricing**: Seasonal rates, special offers, group discounts
- **Operations**: Check-in/out, room service, billing

### Key Concepts to Practice
- Strategy pattern for pricing
- State pattern for booking status
- Factory pattern for room creation
- Template method for booking process

### Expected Classes
- `Room`, `Booking`, `Customer`, `PricingStrategy`, `BookingState`, `Hotel`

---

## Question 8: Splitwise/Bill Sharing ⭐⭐ ✅
**Difficulty**: Medium | **Time**: 5-6 hours | **Status**: ✅ Completed

### Problem Statement
Already implemented in `/MachineCoding/Splitwise/` - will be moved to Examples folder.

---

## Question 9: Chess Game ⭐⭐
**Difficulty**: Medium | **Time**: 6-7 hours | **Status**: ⏳ Pending

### Problem Statement
Design a chess game with complete rule validation, move generation, and game state management.

### Requirements
- **Board**: 8x8 grid with piece positioning
- **Pieces**: All 6 types with unique movement rules
- **Moves**: Validation, special moves (castling, en passant)
- **Game Logic**: Check/checkmate detection, turn management
- **History**: Move recording, undo functionality

### Key Concepts to Practice
- Command pattern for moves
- Strategy pattern for piece movement
- State pattern for game states
- Memento pattern for game history

### Expected Classes
- `Board`, `Piece`, `Move`, `Game`, `Player`, `MoveValidator`, `GameState`

---

## Question 10: Elevator System ⭐⭐
**Difficulty**: Medium | **Time**: 5-6 hours | **Status**: 🔄 In Progress

### Problem Statement
Design an elevator control system for a multi-floor building with multiple elevators.

### Requirements
- **Elevators**: Current floor, direction, capacity, maintenance mode
- **Requests**: Floor requests from inside/outside elevators
- **Scheduling**: Optimal elevator assignment algorithm
- **Safety**: Weight limits, emergency stops, door operations
- **Efficiency**: Minimize wait time and energy consumption

### Key Concepts to Practice
- Strategy pattern for scheduling algorithms
- State pattern for elevator states
- Observer pattern for request notifications
- Singleton pattern for elevator controller

### Expected Classes
- `Elevator`, `ElevatorController`, `Request`, `SchedulingStrategy`, `ElevatorState`

---

## 🎯 Learning Objectives for Intermediate Level

### Advanced Design Patterns
- [ ] Composite Pattern (tree structures)
- [ ] Template Method (algorithm skeleton)
- [ ] Command Pattern (encapsulate requests)
- [ ] Memento Pattern (state restoration)
- [ ] Chain of Responsibility (request handling)

### Complex Business Logic
- [ ] Multi-step workflows
- [ ] State machines
- [ ] Algorithm optimization
- [ ] Concurrent operations
- [ ] Data consistency

### System Integration
- [ ] Multiple interacting components
- [ ] Event-driven architecture
- [ ] Service layer patterns
- [ ] Error propagation
- [ ] Performance considerations

## 📝 Completion Checklist

For each problem, ensure you have:
- [ ] **Complex Requirements**: Handle multiple interacting features
- [ ] **Design Patterns**: Use 3+ patterns appropriately
- [ ] **Error Handling**: Comprehensive exception management
- [ ] **Performance**: Consider time/space complexity
- [ ] **Extensibility**: Design for future requirements
- [ ] **Testing**: Unit tests for critical components
- [ ] **Documentation**: Detailed design decisions and trade-offs

## 🚀 Next Steps
Once you complete all Intermediate Level questions:
1. Practice explaining complex design decisions
2. Optimize for performance and scalability
3. Implement additional features as extensions
4. Move to Advanced Level questions

---

*These problems require deeper understanding of design patterns and complex business logic. Focus on creating extensible and maintainable solutions.*