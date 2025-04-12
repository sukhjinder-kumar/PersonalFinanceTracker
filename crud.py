import sqlite3
from typing import Optional, List, Tuple, Any


class FinanceDB:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def _execute(self, query: str, params: Tuple = (), fetch: str = "none") -> Optional[List[Tuple]]:
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch == "all":
                return cursor.fetchall()
            elif fetch == "one":
                return cursor.fetchone()
            conn.commit()

    # ---- Accounts ----
    def create_account(self, name: str, acc_type: str):
        self._execute("INSERT INTO accounts (name, type) VALUES (?, ?)", (name, acc_type))

    def get_accounts(self) -> List[Tuple]:
        return self._execute("SELECT * FROM accounts", fetch="all")

    def update_account(self, acc_id: int, name: Optional[str], acc_type: Optional[str]):
        if name:
            self._execute("UPDATE accounts SET name = ? WHERE id = ?", (name, acc_id))
        if acc_type:
            self._execute("UPDATE accounts SET type = ? WHERE id = ?", (acc_type, acc_id))

    def delete_account(self, acc_id: int):
        self._execute("DELETE FROM accounts WHERE id = ?", (acc_id,))

    # ---- Categories ----
    def create_category(self, name: str, parent_id: Optional[int]):
        self._execute("INSERT INTO categories (name, parent_id) VALUES (?, ?)", (name, parent_id))

    def get_categories(self) -> List[Tuple]:
        return self._execute("SELECT * FROM categories", fetch="all")

    def update_category(self, cat_id: int, name: Optional[str], parent_id: Optional[int]):
        if name:
            self._execute("UPDATE categories SET name = ? WHERE id = ?", (name, cat_id))
        if parent_id is not None:
            self._execute("UPDATE categories SET parent_id = ? WHERE id = ?", (parent_id, cat_id))

    def delete_category(self, cat_id: int):
        self._execute("DELETE FROM categories WHERE id = ?", (cat_id,))

    # ---- Transactions ----
    def create_transaction(self, date: str, amount: float, description: str,
                           category_id: Optional[int], account_id: Optional[int]):
        self._execute("""
            INSERT INTO transactions (date, amount, description, category_id, account_id)
            VALUES (?, ?, ?, ?, ?)
        """, (date, amount, description, category_id, account_id))

    def get_transactions(self) -> List[Tuple]:
        return self._execute("SELECT * FROM transactions", fetch="all")

    def update_transaction(self, tx_id: int, **kwargs):
        for field in ['date', 'amount', 'description', 'category_id', 'account_id']:
            if field in kwargs:
                self._execute(f"UPDATE transactions SET {field} = ? WHERE id = ?", (kwargs[field], tx_id))

    def delete_transaction(self, tx_id: int):
        self._execute("DELETE FROM transactions WHERE id = ?", (tx_id,))

    # ---- Recurring ----
    def create_recurring(self, description: str, amount: float, frequency: str, next_due: str,
                         category_id: Optional[int], account_id: Optional[int]):
        self._execute("""
            INSERT INTO recurring (description, amount, frequency, next_due, category_id, account_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (description, amount, frequency, next_due, category_id, account_id))

    def get_recurring(self) -> List[Tuple]:
        return self._execute("SELECT * FROM recurring", fetch="all")

    def update_recurring(self, rec_id: int, **kwargs):
        for field in ['description', 'amount', 'frequency', 'next_due', 'category_id', 'account_id']:
            if field in kwargs:
                self._execute(f"UPDATE recurring SET {field} = ? WHERE id = ?", (kwargs[field], rec_id))

    def delete_recurring(self, rec_id: int):
        self._execute("DELETE FROM recurring WHERE id = ?", (rec_id,))

    # ---- Tags ----
    def create_tag(self, name: str):
        self._execute("INSERT INTO tags (name) VALUES (?)", (name,))

    def get_tags(self) -> List[Tuple]:
        return self._execute("SELECT * FROM tags", fetch="all")

    def update_tag(self, tag_id: int, name: str):
        self._execute("UPDATE tags SET name = ? WHERE id = ?", (name, tag_id))

    def delete_tag(self, tag_id: int):
        self._execute("DELETE FROM tags WHERE id = ?", (tag_id,))

    # ---- Transaction_Tags ----
    def add_tag_to_transaction(self, transaction_id: int, tag_id: int):
        self._execute("INSERT OR IGNORE INTO transaction_tags (transaction_id, tag_id) VALUES (?, ?)",
                      (transaction_id, tag_id))

    def remove_tag_from_transaction(self, transaction_id: int, tag_id: int):
        self._execute("DELETE FROM transaction_tags WHERE transaction_id = ? AND tag_id = ?",
                      (transaction_id, tag_id))

    def get_transaction_tags(self, transaction_id: int) -> List[Tuple]:
        return self._execute("""
            SELECT tags.id, tags.name
            FROM tags
            JOIN transaction_tags ON tags.id = transaction_tags.tag_id
            WHERE transaction_tags.transaction_id = ?
        """, (transaction_id,), fetch="all")
