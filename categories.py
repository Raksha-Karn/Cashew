class CategoryManager:
    def __init__(self):
        self.categories = {
            "Income": [],
            "Expense": []
        }

    def add_categories(self):
        while True:
            choice = input(
                "\nEnter:\n"
                "1. Add Income Category\n"
                "2. Add Expense Category\n"
                "3. Exit\n"
                "Choice: "
            )

            if choice == "3":
                break

            if choice not in ["1", "2"]:
                print("Invalid input. Try again.")
                continue

            category_type = "Income" if choice == "1" else "Expense"

            example = "salary, stipend" if choice == "1" else "food, rent"
            category = input(f"Enter {category_type} Category (ex. {example}): ").title()

            if category in self.categories[category_type]:
                print("Category already exists!")
                continue

            self.categories[category_type].append(category)
            print(f"{category_type} category added successfully!")

    def view_all_categories(self):
        pass

    def view_categories_by_type(self, category_type):
        pass

    def remove_categories(self):
        print("Take a look at all of the categories! ")
        self.view_all_categories()
        while True:
            choice = input("Enter type of category to remove from: \n1.Income\n2.Expense\n3.Exit")
            if choice == "3":
                break
            if choice not in ["1", "2", "3"]:
                print("Invalid input. Try again.")
                continue

            category_type = "Income" if choice == "1" else "Expense"
            
            self.view_categories_by_type(category_type)
            while True: 
                category = input("Enter category to remove: ").title()
                if category in self.categories[category_type]:
                    self.categories[category_type].remove(category)
                    break
                else:
                    print("Category does not exist!")
            
