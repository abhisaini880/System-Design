from services.userService import UserService
from services.groupService import GroupService
from services.paymentService import PaymentService
from services.expenseService import ExpenseService


def handler(args_list):
    service_handler = {
        "1": GroupService,
        "2": UserService,
        "3": GroupService,
        "4": ExpenseService,
        "5": PaymentService,
        "6": None,
        "7": GroupService,
        "8": GroupService,
    }

    service = service_handler[args_list[0]]

    # TODO: use if else to imprlement logic for each choice.


def main():
    while True:
        print(
            "\n\n============================================================================"
        )
        print("Expense Sharing APP")
        print(
            "============================================================================"
        )
        print("1. Create Group [name]")
        print("2. Create user [name, mobile_number]")
        print("3. Add Member [group, user]")
        print("4. Add Expense [group, amount, description, paid_by]")
        print(
            "5. Pay Expense [group, amount, paid_by, paid_to, payment_method]"
        )
        print("6. Show Expenses [group]")
        print("7. Show Balances [group]")
        print("8. Close Group [group]")
        print("9. Exit")
        print(
            "============================================================================\n"
        )

        choice = input("Enter your choice (1-9): \n").split()

        try:
            if int(choice[0]) < 9:
                handler(choice)

            elif choice[0] == "9":
                print("Exiting the application. Goodbye!")
                break

            else:
                print(
                    "Invalid choice. Please enter a number between 1 and 9."
                )
        except Exception:
            print("Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()
