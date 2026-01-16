import json
import csv


def load_from_file():
    try:
        with open("expenses.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_to_file(expenses):
    with open("expenses.json", "w") as f:
        json.dump(expenses, f, indent=4)
    print("Expenses saved!")


def load_budget():
    try:
        with open("budget.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_budget(budget):
    with open("budget.json", "w") as f:
        json.dump(budget, f, indent=4)



def show_menu():
    print("\n=== Expense Tracker ===")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View by Category")
    print("4. Monthly Summary")
    print("5. Delete Expense")
    print("6. Save & Exit")
    print("7. Set Monthly Budget")
    print("8. Check Budget Status")
    print("9. Export Expenses to CSV")



def add_expense(expenses):
    try:
        amount = float(input("Enter amount: $"))
        if amount <= 0:
            print("Amount must be positive!")
            return
    except ValueError:
        print("Invalid amount!")
        return

    category = input("Enter category (Food/Transport/Entertainment/Other): ").capitalize()
    description = input("Enter description: ")
    date = input("Enter date (YYYY-MM-DD): ")

    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }

    expenses.append(expense)
    print("Expense added successfully!")

    # Budget warning
    budget = load_budget()
    month = date[:7]

    if month in budget:
        total = sum(exp["amount"] for exp in expenses if exp["date"].startswith(month))
        if total > budget[month]:
            print("  WARNING: Monthly budget exceeded!")


def view_all_expenses(expenses):
    if not expenses:
        print("No expenses found!")
        return

    print("\n=== All Expenses ===")
    for i, exp in enumerate(expenses, start=1):
        print(f"{i}. ${exp['amount']:.2f} - {exp['category']} - {exp['description']} ({exp['date']})")


def view_by_category(expenses):
    cat = input("Enter category: ").capitalize()
    found = False

    for exp in expenses:
        if exp["category"] == cat:
            print(f"{exp['date']} | {exp['category']} | ${exp['amount']:.2f} | {exp['description']}")
            found = True

    if not found:
        print("No expenses found in this category.")


def monthly_summary(expenses):
    month = input("Enter month (YYYY-MM): ")
    total = sum(exp["amount"] for exp in expenses if exp["date"].startswith(month))

    if total == 0:
        print("No expenses for this month.")
    else:
        print(f"Total spent in {month}: ${total:.2f}")


def delete_expense(expenses):
    view_all_expenses(expenses)
    if not expenses:
        return

    try:
        index = int(input("Enter expense number to delete: ")) - 1
        removed = expenses.pop(index)
        print("Deleted:", removed)
    except (ValueError, IndexError):
        print("Invalid selection!")


def set_budget():
    budget = load_budget()
    month = input("Enter month (YYYY-MM): ")

    try:
        limit = float(input("Enter budget limit: $"))
        if limit <= 0:
            print("Budget must be positive!")
            return
    except ValueError:
        print("Invalid amount!")
        return

    budget[month] = limit
    save_budget(budget)
    print(f"Budget set for {month}: ${limit:.2f}")


def check_budget(expenses):
    budget = load_budget()
    month = input("Enter month (YYYY-MM): ")

    if month not in budget:
        print("No budget set for this month.")
        return

    spent = sum(exp["amount"] for exp in expenses if exp["date"].startswith(month))
    limit = budget[month]
    remaining = limit - spent

    print(f"\nBudget for {month}: ${limit:.2f}")
    print(f"Spent: ${spent:.2f}")

    if remaining < 0:
        print(f"  Budget exceeded by ${abs(remaining):.2f}")
    else:
        print(f"Remaining budget: ${remaining:.2f}")


def export_to_csv(expenses):
    if not expenses:
        print("No expenses to export!")
        return

    with open("expenses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Amount", "Category", "Description", "Date"])

        for exp in expenses:
            writer.writerow([
                exp["amount"],
                exp["category"],
                exp["description"],
                exp["date"]
            ])

    print("Expenses exported to expenses.csv successfully!")




def main():
    expenses = load_from_file()

    while True:
        show_menu()
        choice = input("Choose an option (1-9): ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_all_expenses(expenses)

        elif choice == "3":
            view_by_category(expenses)

        elif choice == "4":
            monthly_summary(expenses)

        elif choice == "5":
            delete_expense(expenses)

        elif choice == "6":
            save_to_file(expenses)
            print("Goodbye!")
            break

        elif choice == "7":
            set_budget()

        elif choice == "8":
            check_budget(expenses)

        elif choice == "9":
            export_to_csv(expenses)

        else:
            print("Invalid choice!")


main()
