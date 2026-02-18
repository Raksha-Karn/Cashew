import datetime
import uuid
import csv
import json

DATA_FILE = "finance_data.json"

class TransactionManager:
    def __init__(self, initial_balance, budget, category_manager):
        self.balance = initial_balance
        self.budget = budget
        self.transactions = {
            "Income": [],
            "Expense": []
        }
        self.category_manager = category_manager

    def add_transaction(self):
        while True:
            choice = input("Enter Type of Transaction(Income/Expense)\nEnter(1-2)\n1.Income\n2.Expense\n3.Exit").strip()
            if choice == "3":
                break
            if choice not in ["1","2"]:
                print("Invalid input. Enter 1 for Income or 2 for Expense or 3 to exit.")
                continue

            category_type = "Income" if choice == "1" else "Expense"
            example = "salary, stipend" if choice == "1" else "food, rent"
            print(f"\nAvailable {category_type} Categories:")
            if self.category_manager.categories[category_type]:
                for i, cat in enumerate(self.category_manager.categories[category_type], start=1):
                    print(f"{i}. {cat}")
                category = input(f"Enter category number or type a new category (ex. {example}): ").title()
            else: 
                category = input(f"Category (ex. {example}): ")

            if category.isdigit():
                index = int(category) - 1
                if 0 <= index < len(self.category_manager.categories[category_type]):
                    category = self.category_manager.categories[category_type][index]
                else:
                    print("Invalid number, try again.")
                    continue
            else:
                category = category.title()
                self.category_manager.categories[category_type].append(category)
                print(f"New {category_type} category '{category}' created and linked!")

            while True:
                try:
                    amount = float(input("Amount: "))
                    if amount <= 0:
                        print("Amount must be positive. Try again!")
                        continue
                    break
                except ValueError:
                    print("Amount must be a number!")
            description = input("Desc (ex. Brunch at Patan Rooftop Cafe) (Optional): ").strip()
            while True:
                issued_date_input = input("Date (YYYY-MM-DD) or press Enter for today: ").strip()
                if issued_date_input == "":
                    issued_date = datetime.date.today()
                    break
                else:
                    try:
                        issued_date = datetime.datetime.strptime(issued_date_input, "%Y-%m-%d").date()
                        break
                    except ValueError:
                        print("Invalid date format! Use YYYY-MM-DD. Try again!")

            transaction = {
                "Id": str(uuid.uuid4()),
                "Category": category,
                "Type": category_type,
                "Amount": amount,
                "Description": description,
                "Date": issued_date
            }
            
            self.transactions[category_type].append(transaction)
            if category_type == "Income":
                self.balance += amount
            else:
                self.balance -= amount

                today = datetime.date.today()

                monthly_expense = sum(
                        txn["Amount"]
                        for txn in self.transactions["Expense"]
                        if txn["Date"].year == today.year and txn["Date"].month == today.month
                )

                if monthly_expense > self.budget:
                    print("Monthly budget exceeded!")


            print("\nTransaction added successfully! Details:")
            print(f"ID         : {transaction['Id']}")
            print(f"Type       : {transaction['Type']}")
            print(f"Category   : {transaction['Category']}")
            print(f"Amount     : {transaction['Amount']:.2f}")
            print(f"Description: {transaction['Description'] if description else 'None'}")
            print(f"Date       : {transaction['Date']}")
            print(f"Current Balance: ${self.balance:.2f}\n")

            self.save_to_file(DATA_FILE)



    def view_all_transactions(self, sort_by_category=False):
        all_transactions = self.transactions["Income"] + self.transactions["Expense"]

        if not all_transactions:
            print("\nNo transactions to show.")
            return

        if sort_by_category:
            all_transactions = sorted(all_transactions, key=lambda x: x["Category"])

        print("\n| ID                                   | Type    | Category        | Amount     | Description                      | Date       |")
        print("|--------------------------------------+---------|----------------|------------|----------------------------------|------------|")

        for txn in all_transactions:
            txn_id = str(txn["Id"])[:8]  
            txn_type = txn["Type"]
            category = txn["Category"]
            amount = f"{txn['Amount']:.2f}"
            desc = txn["Description"] if txn["Description"] else "None"
            date = txn["Date"]

            print(f"| {txn_id:<36} | {txn_type:<7} | {category:<14} | {amount:<10} | {desc:<32} | {date} |")

        print("|--------------------------------------+---------|----------------|------------|----------------------------------|------------|")

    def view_transaction_summary(self):
        income_transactions = sum(transaction["Amount"] for transaction in self.transactions["Income"])
        expense_transactions = sum(transaction["Amount"] for transaction in self.transactions["Expense"])
        
        print("\n===== FINANCIAL SUMMARY =====")
        print(f"Total Income : ${income_transactions:.2f}")
        print(f"Total Expense: ${expense_transactions:.2f}")
        print(f"Balance      : ${self.balance:.2f}")
        print(f"Transactions : {len(self.transactions['Income']) + len(self.transactions['Expense'])}")
        print("=============================\n")

    def filter_transactions(self):
        all_transactions = self.transactions["Income"] + self.transactions["Expense"]

        if not all_transactions:
            print("\nNo transactions available.")
            return

        print("\nFilter By:")
        print("1. Type (Income / Expense)")
        print("2. Category")
        print("3. Date Range")
        print("4. Amount Range")
        print("5. Back")

        choice = input("Select option (1-5): ").strip()

        filtered = all_transactions

        if choice == "1":
            txn_type = input("Enter type (Income/Expense): ").title()
            if txn_type not in ["Income", "Expense"]:
                print("Invalid type.")
                return
            filtered = [txn for txn in filtered if txn["Type"] == txn_type]

        elif choice == "2":
            category = input("Enter category: ").title()
            filtered = [txn for txn in filtered if txn["Category"] == category]

        elif choice == "3":
            import datetime
            try:
                start_input = input("Start date (YYYY-MM-DD): ")
                end_input = input("End date (YYYY-MM-DD): ")

                start_date = datetime.datetime.strptime(start_input, "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(end_input, "%Y-%m-%d").date()

                filtered = [
                    txn for txn in filtered
                    if start_date <= txn["Date"] <= end_date
                ]
            except ValueError:
                print("Invalid date format.")
                return

        elif choice == "4":
            try:
                min_amount = float(input("Minimum amount: "))
                max_amount = float(input("Maximum amount: "))

                filtered = [
                    txn for txn in filtered
                    if min_amount <= txn["Amount"] <= max_amount
                ]
            except ValueError:
                print("Invalid amount input.")
                return

        elif choice == "5":
            return

        else:
            print("Invalid option.")
            return

        if not filtered:
            print("\nNo matching transactions found.")
            return

        print("\n===== FILTERED TRANSACTIONS =====")
        for txn in filtered:
            print(f"{txn['Date']} | {txn['Type']} | {txn['Category']} | ${txn['Amount']:.2f} | {txn['Description']}")
        print("=================================\n")


    def export_to_csv(self, filename="transactions.csv"):
        all_transactions = self.transactions["Income"] + self.transactions["Expense"]

        if not all_transactions:
            print("No transactions to export.")
            return

        with open(filename, mode="w", newline="") as file:
            fieldnames = ["ID", "Type", "Category", "Amount", "Description", "Date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for txn in all_transactions:
                writer.writerow([
                    writer.writerow({
                        "ID": txn["Id"],
                        "Type": txn["Type"],
                        "Category": txn["Category"],
                        "Amount": txn["Amount"],
                        "Description": txn["Description"],
                        "Date": txn["Date"]
                    })

                ])

        print(f"Transactions exported successfully to {filename}")


    def monthly_report(self):
        from collections import defaultdict

        all_transactions = self.transactions["Income"] + self.transactions["Expense"]

        if not all_transactions:
            print("\nNo transactions available to generate report.")
            return

        try:
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (1-12): "))

            if month < 1 or month > 12:
                print("Invalid month. Must be between 1 and 12.")
                return

        except ValueError:
            print("Invalid input. Year and month must be numbers.")
            return

        current_month_txns = [
            txn for txn in all_transactions
            if txn["Date"].year == year and txn["Date"].month == month
        ]

        if not current_month_txns:
            print("\nNo transactions found for this month.")
            return

        total_income = 0
        total_expense = 0

        income_by_category = defaultdict(float)
        expense_by_category = defaultdict(float)

        for txn in current_month_txns:
            if txn["Type"] == "Income":
                total_income += txn["Amount"]
                income_by_category[txn["Category"]] += txn["Amount"]
            else:
                total_expense += txn["Amount"]
                expense_by_category[txn["Category"]] += txn["Amount"]

        print(f"\n===== MONTHLY REPORT: {year}-{month:02d} =====")
        print(f"Total Income : ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Net Savings  : ${(total_income - total_expense):.2f}")
        print("--------------------------------------------")

        print("\nExpense Breakdown by Category:")
        if expense_by_category:
            print("\nExpense Breakdown by Category:")
            for category, amount in expense_by_category.items():
                print(f"{category}: ${amount:.2f}")
        else:
            print("\nNo expenses recorded this month.")

        if expense_by_category:
            highest_category = max(expense_by_category, key=expense_by_category.get)
            highest_amount = expense_by_category[highest_category]
            print(f"\nHighest Expense Category: {highest_category} (${highest_amount:.2f})")
        else:
            print("\nNo expenses recorded this month.")

        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year

        previous_month_txns = [
            txn for txn in all_transactions
            if txn["Date"].year == prev_year and txn["Date"].month == prev_month
        ]

        if not previous_month_txns:
            print("\nNo data available for previous month comparison.")
        else:
            prev_income = sum(
                txn["Amount"] for txn in previous_month_txns
                if txn["Type"] == "Income"
            )
            prev_expense = sum(
                txn["Amount"] for txn in previous_month_txns
                if txn["Type"] == "Expense"
            )

            print("\n----- Comparison with Previous Month -----")
            print(f"Previous Month ({prev_year}-{prev_month:02d})")
            print(f"Income Change : ${total_income - prev_income:.2f}")
            print(f"Expense Change: ${total_expense - prev_expense:.2f}")

        print("==========================================\n")

    def save_to_file(self, filename="finance_data.json"):
        data = {
            "balance": self.balance,
            "budget": self.budget,
            "transactions": {
                "Income": [],
                "Expense": []
            }
        }

        for txn_type in ["Income", "Expense"]:
            for txn in self.transactions[txn_type]:
                txn_copy = txn.copy()
                txn_copy["Date"] = txn_copy["Date"].isoformat()
                data["transactions"][txn_type].append(txn_copy)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_from_file(self, filename="finance_data.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)

            self.balance = data["balance"]
            self.budget = data["budget"]
            self.transactions = {"Income": [], "Expense": []}

            for txn_type in ["Income", "Expense"]:
                for txn in data["transactions"][txn_type]:
                    txn["Date"] = datetime.datetime.strptime(
                        txn["Date"], "%Y-%m-%d"
                    ).date()
                    self.transactions[txn_type].append(txn)

            print("Data loaded successfully.")

        except FileNotFoundError:
            print("No previous data found. Starting fresh.")


