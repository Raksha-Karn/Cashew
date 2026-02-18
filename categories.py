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
            ).strip()

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
        print("\n|   Type    |      Category       |")
        print("|-----------|---------------------|")

        if not self.categories["Income"]:
            print(f"| {'Income':<9} | {'No categories':<19} |")

        if not self.categories["Expense"]:
            print(f"| {'Expense':<9} | {'No categories':<19} |")

        for category in self.categories["Income"]:
            print(f"| {'Income':<9} | {category:<19} |")

        for category in self.categories["Expense"]:
            print(f"| {'Expense':<9} | {category:<19} |")

        print("|-----------|---------------------|")

    def view_categories_by_type(self, category_type):
        print(f"\n|   {category_type} Categories   |")
        print("|-------------------------------|")

        if not self.categories[category_type]:
            print("|        No categories          |")
        else:
            for category in self.categories[category_type]:
                print(f"| {category:<29} |")

        print("|-------------------------------|")


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
            if not self.categories[category_type]:
                print("No categories to remove.")
                continue

            while True: 
                category = input("Enter category to remove: ").title()
                if category in self.categories[category_type]:
                    self.categories[category_type].remove(category)
                    print("Category removed successfully!")
                    break
                else:
                    print("Category does not exist!")


category_manager = CategoryManager()

while True:
    try:
        option = input(
            "\nWhat would you like to do?\n"
            "1. Add Category\n"
            "2. Remove Category\n"
            "3. View All Categories\n"
            "4. View Categories By Type\n"
            "5. Exit\n"
            "Choice: "
        )
    except ValueError:
        print("Invalid input! Please enter a number (1-5).")
        continue

    if option == "5":
        print("Exiting...")
        break

    if option == "1":
        category_manager.add_categories()
    elif option == "2":
        category_manager.remove_categories()
    elif option == "3":
        category_manager.view_all_categories()
    elif option == "4":
        type_choice = input("Enter type (Income/Expense): ").title()
        if type_choice not in ["Income", "Expense"]:
            print("Invalid type!")
            continue
        category_manager.view_categories_by_type(type_choice)
  



            
