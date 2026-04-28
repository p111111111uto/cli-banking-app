import json, csv
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / 'data' / 'accounts.json'
CSV_FILE = Path(__file__).resolve().parent / 'data' / 'transactions.csv'
FIELDS = ['transaction_id', 'account_number', 'type', 'amount', 'date', 'description']


def load_accounts():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            # File exists but is empty or corrupt — start fresh
            return {}
    return {}


def save_accounts(accounts):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(accounts, file, indent=2)


def load_transactions():
    if CSV_FILE.exists():
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    return []


def save_transaction(transaction):
    # Check both existence AND size: an empty file has no header row yet
    file_exists = CSV_FILE.exists() and CSV_FILE.stat().st_size > 0
    # Append mode so previous transactions are never overwritten
    with open(CSV_FILE, 'a', newline='') as file:
        # newline='' is required by the csv module to prevent extra blank
        # lines being inserted on Windows
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(transaction)
