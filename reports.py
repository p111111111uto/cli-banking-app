from pathlib import Path
from storage import load_accounts, load_transactions
from utils import get_user_accounts

TXT_FILE = Path(__file__).resolve().parent / 'data' / 'report.txt'


def sort_transactions(transactions, key='date', reverse=False):
    # Bubble sort: repeatedly compare adjacent pairs and swap if out of order.
    # After each full pass the largest unsorted element is in its final position,
    # so the inner loop shrinks by one each time (range(n - i - 1)).
    txs = list(transactions)
    n = len(txs)
    for i in range(n - 1):
        for j in range(n - i - 1):
            a = txs[j][key]
            b = txs[j + 1][key]
            # CSV stores all values as strings, so cast amounts to float before comparing
            if key == 'amount':
                a, b = float(a), float(b)
            # (a > b) != reverse flips the condition when sorting descending:
            #   reverse=False → swap when a > b  (ascending)
            #   reverse=True  → swap when a <= b (descending)
            if (a > b) != reverse:
                txs[j], txs[j + 1] = txs[j + 1], txs[j]
    return txs


def search_transactions(transactions, keyword):
    # Linear search: scan every transaction and collect any that contain
    # the keyword in the ID, type, description, or amount fields
    keyword = keyword.lower()
    results = []
    for t in transactions:
        if (keyword in t.get('transaction_id', '').lower()
                or keyword in t.get('type', '').lower()
                or keyword in t.get('description', '').lower()
                or keyword in str(t.get('amount', '')).lower()):
            results.append(t)
    return results


def generate_report(username):
    accounts = load_accounts()
    user_accounts = get_user_accounts(accounts, username)
    transactions = load_transactions()
    # Build a set of account numbers for O(1) membership checks in the loop below
    user_acc_nums = set(user_accounts.keys())
    user_txs = [t for t in transactions if t['account_number'] in user_acc_nums]

    total = sum(acc['balance'] for acc in user_accounts.values())
    total_deposits = sum(float(t['amount']) for t in user_txs if t['type'] == 'deposit')
    total_withdrawals = sum(float(t['amount']) for t in user_txs if t['type'] == 'withdrawal')
    total_transfers_out = sum(float(t['amount']) for t in user_txs if t['type'] == 'transfer_out')

    print(f'\n{"=" * 45}')
    print(f'  Account Report — {username}')
    print(f'{"=" * 45}')
    for acc_num, acc in user_accounts.items():
        print(f'  {acc_num}  ({acc["type"].capitalize()})  ${acc["balance"]:.2f}')
    print(f'  Total balance:      ${total:.2f}')
    print(f'  Total deposited:    ${total_deposits:.2f}')
    print(f'  Total withdrawn:    ${total_withdrawals:.2f}')
    print(f'  Total transferred:  ${total_transfers_out:.2f}')
    print(f'  Transactions:       {len(user_txs)}')
    print(f'{"=" * 45}')


def export_to_txt(username):
    accounts = load_accounts()
    user_accounts = get_user_accounts(accounts, username)
    transactions = load_transactions()
    user_acc_nums = set(user_accounts.keys())
    user_txs = [t for t in transactions if t['account_number'] in user_acc_nums]
    # Sort newest-first so the exported file is easiest to read
    user_txs = sort_transactions(user_txs, 'date', reverse=True)

    with open(TXT_FILE, 'w', encoding='utf-8') as f:
        f.write(f'Transaction Report — {username}\n')
        f.write('=' * 60 + '\n')
        for t in user_txs:
            line = (
                f'[{t.get("transaction_id", "N/A")}] '
                f'{t["date"]} | {t["account_number"]} | '
                f'{t["type"].upper()} | '
                f'${float(t["amount"]):.2f} | '
                f'{t.get("description", "")}\n'
            )
            f.write(line)

    print(f'Exported {len(user_txs)} transaction(s) to {TXT_FILE}')
