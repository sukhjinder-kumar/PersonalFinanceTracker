from crud import FinanceDB
from schema import initialize_database
from datetime import datetime, timedelta
import random
import os

def populate_sample_data(db_name):
    db = FinanceDB(db_name)

    # Sample accounts
    accounts = [
        ("Cash Wallet", "cash"),
        ("HDFC Debit Card", "debit"),
        ("ICICI Credit Card", "credit"),
        ("Zerodha Investments", "investment")
    ]
    for name, acc_type in accounts:
        db.create_account(name, acc_type)

    # Sample categories (with hierarchy)
    db.create_category("Housing", None)
    db.create_category("Groceries", None)
    db.create_category("Transport", None)
    db.create_category("Utilities", None)
    db.create_category("Electricity", 4)
    db.create_category("Water", 4)
    db.create_category("Internet", 4)

    # Sample tags
    tags = ["urgent", "monthly", "health", "fun", "reimbursable"]
    for tag in tags:
        db.create_tag(tag)

    # Sample recurring items
    db.create_recurring("Rent", 18000, "monthly", "2025-05-01", 1, 2)
    db.create_recurring("Internet Bill", 999, "monthly", "2025-05-02", 7, 2)
    db.create_recurring("Gym Membership", 1200, "monthly", "2025-05-03", 1, 1)

    # Sample transactions (30 days of history)
    descriptions = [
        "Uber ride", "Amazon order", "Electricity bill", "Local grocery",
        "Cinema ticket", "Restaurant", "Bus pass", "Doctor visit", "Mobile recharge"
    ]

    for i in range(30):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        amount = round(random.uniform(100, 2000), 2)
        description = random.choice(descriptions)
        category_id = random.randint(2, 7)
        account_id = random.randint(1, 4)

        db.create_transaction(date, amount, description, category_id, account_id)

        # Randomly tag transactions
        if random.random() < 0.5:
            tag_id = random.randint(1, len(tags))
            db.add_tag_to_transaction(i + 1, tag_id)

    print("Sample data populated successfully.")

if __name__ == "__main__":
    db_name = "finance_tracker.db"

    # Delete old DB
    if os.path.exists(db_name):
        os.remove(db_name)
        print("Database deleted.")

    initialize_database(db_name)
    populate_sample_data(db_name)
