import datetime
import uuid


class TransactionManager:
    def __init__(self):
        self.balance = 0
        self.transactions = {
            "Income": [],
            "Expense": []
        }

    def add_transaction(self):
        while True:
            choice = input("Enter Type of Transaction(Income/Expense)\nEnter(1-2)\n1.Income\n2.Expense\n3.Exit")
            if choice == "3":
                break
            if choice not in ["1","2"]:
                print("Invalid input. Enter 1 for Income or 2 for Expense or 3 to exit.")
                continue

            category_type = "Income" if choice == "1" else "Expense"
            example = "salary, stipend" if choice == "1" else "food, rent"
            category = input(f"Enter {category_type} Category (ex. {example}): ").title()
            while True:
                try:
                    amount = float("Amount: ")
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
                "Id": uuid.uuid4(),
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
            print("Transaction added successfully!")
            print(f"Your Balance: {self.balance:.2f}")


    def transaction_info(self):
        pass
