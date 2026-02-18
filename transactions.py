import datetime
import uuid


class TransactionManager:
    def __init__(self, budget, category_manager):
        self.balance = 0
        self.transactions = {
            "Income": [],
            "Expense": []
        }
        self.budget = budget
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
            print("\nTransaction added successfully! Details:")
            print(f"ID         : {transaction['Id']}")
            print(f"Type       : {transaction['Type']}")
            print(f"Category   : {transaction['Category']}")
            print(f"Amount     : {transaction['Amount']:.2f}")
            print(f"Description: {transaction['Description'] if description else 'None'}")
            print(f"Date       : {transaction['Date']}")
            print(f"Current Balance: ${self.balance:.2f}\n")


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

