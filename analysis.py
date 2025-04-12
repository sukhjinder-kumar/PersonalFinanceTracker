import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

DB_NAME = "finance_tracker.db"

def load_transactions(db_name: str = DB_NAME) -> pd.DataFrame:
    with sqlite3.connect(db_name) as conn:
        df = pd.read_sql_query("""
            SELECT 
                t.id AS transaction_id,
                t.date,
                t.amount,
                t.description,
                c.name AS category,
                a.name AS account,
                a.type AS account_type
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN accounts a ON t.account_id = a.id
        """, conn, parse_dates=["date"])
    return df


def monthly_spending_by_category(df: pd.DataFrame) -> pd.DataFrame:
    df["month"] = df["date"].dt.to_period("M")
    result = df.groupby(["month", "category"])["amount"].sum().unstack(fill_value=0)
    return result


def monthly_spending_by_account(df: pd.DataFrame) -> pd.DataFrame:
    df["month"] = df["date"].dt.to_period("M")
    result = df.groupby(["month", "account"])["amount"].sum().unstack(fill_value=0)
    return result


def total_spending_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("account")[["amount"]].sum().sort_values("amount", ascending=False)


def recent_transactions(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return df.sort_values("date", ascending=False).head(n)


def plot_summary(df: pd.DataFrame, kind: str = "bar"):
    sns.set(style="whitegrid")

    summary = monthly_spending_by_category(df)
    summary.plot(kind=kind, figsize=(12, 6), title="Monthly Spending by Category")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig('Images/monthly_spending_by_category.png')  # Save inside container to shared volume
    plt.show()


def run_all_analyses():
    df = load_transactions()

    print("\n🔹 Recent Transactions:")
    print(recent_transactions(df))

    print("\n🔹 Total Spending per Account:")
    print(total_spending_summary(df))

    print("\n🔹 Monthly Spending by Category:")
    print(monthly_spending_by_category(df))

    print("\n🔹 Monthly Spending by Account:")
    print(monthly_spending_by_account(df))

    # Optional: Plot
    plot_summary(df)


if __name__ == "__main__":
    run_all_analyses()
