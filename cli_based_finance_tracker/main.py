import os
from cli_based_finance_tracker.categories import CategoryManager  
from cli_based_finance_tracker.transactions import TransactionManager  

DATA_FILE = "finance_data.json"


def main():
    category_manager = CategoryManager()

    if os.path.exists(DATA_FILE):
        transaction_manager = TransactionManager(0, 0, category_manager)
        transaction_manager.load_from_file(DATA_FILE)
        print("Loaded previous data successfully!\n")
    else:
        print("Welcome! Let's set up your account.")
        while True:
            try:
                initial_balance = float(input("Enter your starting balance: "))
                if initial_balance < 0:
                    print("Balance cannot be negative.")
                    continue
                break
            except ValueError:
                print("Invalid input. Enter a number.")

        while True:
            try:
                budget = float(input("Enter your monthly budget: "))
                if budget < 0:
                    print("Budget cannot be negative.")
                    continue
                break
            except ValueError:
                print("Invalid input. Enter a number.")

        transaction_manager = TransactionManager(initial_balance, budget, category_manager)
        transaction_manager.save_to_file(DATA_FILE)
        print("Setup complete!\n")

    while True:
        print("\n================================")
        print("     PERSONAL FINANCE TRACKER     ")
        print("================================")
        print(f"Current Balance: ${transaction_manager.balance:.2f}\n")

        print("--- MAIN MENU ---")
        print("0. Add Transactions")
        print("1. View All Transactions")
        print("2. Manage Transaction Category")
        print("3. View Categories")
        print("4. View Summary")
        print("5. Filter Transactions")
        print("6. Monthly Report")
        print("7. Export to CSV")
        print("8. Exit")

        choice = input("Enter your choice (0-8): ").strip()

        if choice not in [str(i) for i in range(9)]:
            print("Invalid input! Enter a number between 0-8.")
            continue

        if choice == "0":
            transaction_manager.add_transaction()
            transaction_manager.save_to_file(DATA_FILE)
        elif choice == "1":
            sort_choice = input("Sort transactions by category? (y/n): ").lower()
            transaction_manager.view_all_transactions(sort_by_category=(sort_choice == "y"))
        elif choice == "2":
            while True:
                cat_choice = input(
                    "\nManage Categories:\n"
                    "1. Add Category\n"
                    "2. Remove Category\n"
                    "3. Back\n"
                    "Choice: "
                ).strip()
                if cat_choice == "1":
                    category_manager.add_categories()
                    transaction_manager.save_to_file(DATA_FILE)
                elif cat_choice == "2":
                    category_manager.remove_categories()
                    transaction_manager.save_to_file(DATA_FILE)
                elif cat_choice == "3":
                    break
                else:
                    print("Invalid input! Choose 1-3.")
        elif choice == "3":
            while True:
                view_choice = input(
                    "\nView Categories:\n"
                    "1. View All Categories\n"
                    "2. View Categories by Type\n"
                    "3. Back\n"
                    "Choice: "
                ).strip()
                if view_choice == "1":
                    category_manager.view_all_categories()
                elif view_choice == "2":
                    type_choice = input("Enter type (Income/Expense): ").title()
                    if type_choice not in ["Income", "Expense"]:
                        print("Invalid type!")
                        continue
                    category_manager.view_categories_by_type(type_choice)
                elif view_choice == "3":
                    break
                else:
                    print("Invalid input! Choose 1-3.")
        elif choice == "4":
            transaction_manager.view_transaction_summary()
        elif choice == "5":
            transaction_manager.filter_transactions()
        elif choice == "6":
            transaction_manager.monthly_report()
        elif choice == "7":
            filename = input("Enter filename (default: transactions.csv): ").strip()
            if filename == "":
                filename = "transactions.csv"
            transaction_manager.export_to_csv(filename + ".csv")
        elif choice == "8":
            print("Exiting... Saving data.")
            transaction_manager.save_to_file(DATA_FILE)
            print("Data saved. Goodbye!")
            break


if __name__ == "__main__":
    main()
