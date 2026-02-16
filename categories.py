categories = {
    "Income": [],
    "Expense": []
}

def add_categories():
    while True:
        choice = input(
            "\nEnter:\n"
            "1. Income Type\n"
            "2. Expense Type\n"
            "3. Exit\n"
            "Choice: "
        )

        if choice == "3":
            break

        if choice not in ["1", "2"]:
            print("Invalid input. Try again.")
            continue

        category_type = "Income" if choice == "1" else "Expense"

        category = input(f"Enter {category_type} Category: ")

        if category in categories[category_type]:
            print("Category already exists!")
            continue

        categories[category_type].append(category)
        print(f"{category_type} category added successfully!")
