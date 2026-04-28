from random import randint

from auth import register, login
from accounts import SavingsAccount
from storage import load_accounts, save_accounts, load_transactions
from transactions import deposit, withdraw, transfer
from reports import generate_report, sort_transactions, search_transactions, export_to_txt
from plotting import plot_balance_history
from utils import get_valid_amount, get_user_accounts, account_to_object


def print_login_menu():
    while True:
        print('\n=== Welcome to PyBank ===')
        print('1. Login\n2. Sign up\n3. Exit')
        try:
            choice = int(input('> '))
            if choice == 1:
                username = login()
                if username:
                    print(f'Welcome back, {username}!')
                    return username
                print('Invalid credentials. Try again.')
            elif choice == 2:
                username = register()
                if username:
                    print(f'Registration complete. Welcome, {username}!')
                    return username
            elif choice == 3:
                print('Goodbye!')
                exit()
            else:
                print('Please enter a valid option.')
        except ValueError:
            print('Please enter a valid option.')


def banking_menu(username):
    while True:
        print(f'\n=== Banking Menu ({username}) ===')
        print('1.  Create account')
        print('2.  Deposit')
        print('3.  Withdraw')
        print('4.  Transfer')
        print('5.  View balance')
        print('6.  View transactions')
        print('7.  Apply interest (savings)')
        print('8.  Search transactions')
        print('9.  Reports & visualization')
        print('10. Logout')
        try:
            choice = int(input('> '))
            if choice == 1:
                create_account(username)
            elif choice == 2:
                do_deposit(username)
            elif choice == 3:
                do_withdraw(username)
            elif choice == 4:
                do_transfer(username)
            elif choice == 5:
                view_balance(username)
            elif choice == 6:
                view_transactions(username)
            elif choice == 7:
                apply_interest(username)
            elif choice == 8:
                do_search(username)
            elif choice == 9:
                reports_menu(username)
            elif choice == 10:
                print(f'Logged out. Goodbye, {username}!')
                break
            else:
                print('Please enter a valid option.')
        except ValueError:
            print('Please enter a valid option.')


def create_account(username):
    print('Account type:\n1. Checking\n2. Savings')
    try:
        acc_type = int(input('> '))
        # Account number stored as a string from the start because JSON
        # serializes all dictionary keys as strings on load
        account_number = str(randint(10000000, 99999999))
        accounts = load_accounts()
        if acc_type == 1:
            accounts[account_number] = {'owner': username, 'balance': 0.0, 'type': 'checking'}
            save_accounts(accounts)
            print(f'Checking account created! Account number: {account_number}')
        elif acc_type == 2:
            accounts[account_number] = {'owner': username, 'balance': 0.0, 'type': 'savings', 'interest_rate': 0.02}
            save_accounts(accounts)
            print(f'Savings account created (2% interest)! Account number: {account_number}')
        else:
            print('Invalid account type.')
    except ValueError:
        print('Please enter a valid option.')


def do_deposit(username):
    accounts = load_accounts()
    user_accounts = get_user_accounts(accounts, username)
    if not user_accounts:
        print('No accounts found. Please create one first.')
        return
    _print_accounts(user_accounts)
    acc_num = input('Account number: ').strip()
    if acc_num not in user_accounts:
        print('Account not found.')
        return
    amount = get_valid_amount()
    # Convert the JSON dict to a class object so deposit() can be called on it
    account = account_to_object(acc_num, accounts[acc_num])
    deposit(account, amount)
    # Write the updated balance back into the accounts dict before saving
    accounts[acc_num]['balance'] = account.balance
    save_accounts(accounts)
    print(f'Deposited ${amount:.2f}. New balance: ${account.balance:.2f}')


def do_withdraw(username):
    accounts = load_accounts()
    user_accounts = get_user_accounts(accounts, username)
    if not user_accounts:
        print('No accounts found.')
        return
    _print_accounts(user_accounts)
    acc_num = input('Account number: ').strip()
    if acc_num not in user_accounts:
        print('Account not found.')
        return
    amount = get_valid_amount()
    account = account_to_object(acc_num, accounts[acc_num])
    if amount > account.balance:
        print('Insufficient funds.')
        return
    withdraw(account, amount)
    accounts[acc_num]['balance'] = account.balance
    save_accounts(accounts)
    print(f'Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}')


def do_transfer(username):
    accounts = load_accounts()
    user_accounts = get_user_accounts(accounts, username)
    if not user_accounts:
        print('No accounts found.')
        return
    _print_accounts(user_accounts)
    from_num = input('Transfer FROM account number: ').strip()
    if from_num not in user_accounts:
        print('Account not found or not yours.')
        return
    to_num = input('Transfer TO account number: ').strip()
    if to_num not in accounts:
        print('Destination account not found.')
        return
    if from_num == to_num:
        print('Cannot transfer to the same account.')
        return
    amount = get_valid_amount()
    from_account = account_to_object(from_num, accounts[from_num])
    if amount > from_account.balance:
        print('Insufficient funds.')
        return
    to_account = account_to_object(to_num, accounts[to_num])
    transfer(from_account, to_account, amount)
    # Both account balances must be written back after a transfer
    accounts[from_num]['balance'] = from_account.balance
    accounts[to_num]['balance'] = to_account.balance
    save_accounts(accounts)
    print(f'Transferred ${amount:.2f} to account {to_num}.')


def view_balance(username):
    accounts = load_accounts()
    user_accounts = get_user_accounts(accounts, username)
    if not user_accounts:
        print('No accounts found.')
        return
    print(f'\n=== Balances for {username} ===')
    total = 0.0
    for acc_num, acc in user_accounts.items():
        print(f'  {acc_num}  ({acc["type"].capitalize()})  ${acc["balance"]:.2f}')
        total += acc['balance']
    print(f'  Total: ${total:.2f}')


def view_transactions(username):
    accounts = load_accounts()
    user_accounts = get_user_accounts(accounts, username)
    user_acc_nums = set(user_accounts.keys())
    transactions = load_transactions()
    # Keep only transactions that belong to this user's accounts
    user_txs = [t for t in transactions if t['account_number'] in user_acc_nums]
    if not user_txs:
        print('No transactions found.')
        return
    print('Sort by:\n1. Date (newest first)\n2. Amount (highest first)\n3. No sort')
    try:
        sort_choice = int(input('> '))
        if sort_choice == 1:
            user_txs = sort_transactions(user_txs, 'date', reverse=True)
        elif sort_choice == 2:
            user_txs = sort_transactions(user_txs, 'amount', reverse=True)
    except ValueError:
        pass
    print(f'\n=== Transaction History ({len(user_txs)} records) ===')
    for t in user_txs:
        print(
            f'  [{t.get("transaction_id", "N/A")}] '
            f'{t["date"]}  {t["account_number"]}  '
            f'{t["type"].upper():<14}  '
            f'${float(t["amount"]):>10.2f}  '
            f'{t.get("description", "")}'
        )


def apply_interest(username):
    accounts = load_accounts()
    user_accounts = get_user_accounts(accounts, username)
    # Interest only applies to savings accounts
    savings = {k: v for k, v in user_accounts.items() if v['type'] == 'savings'}
    if not savings:
        print('No savings accounts found.')
        return
    try:
        periods = int(input('Apply interest for how many periods? '))
        if periods <= 0:
            print('Must be a positive number.')
            return
    except ValueError:
        print('Invalid input.')
        return
    for acc_num, acc_data in savings.items():
        account = SavingsAccount(acc_num, acc_data['balance'], acc_data['owner'], acc_data.get('interest_rate', 0.02))
        old_balance = account.balance
        account.compound_interest(periods)
        earned = account.balance - old_balance
        accounts[acc_num]['balance'] = account.balance
        print(f'  {acc_num}: +${earned:.2f} interest | New balance: ${account.balance:.2f}')
    save_accounts(accounts)


def do_search(username):
    accounts = load_accounts()
    user_accounts = get_user_accounts(accounts, username)
    user_acc_nums = set(user_accounts.keys())
    transactions = load_transactions()
    user_txs = [t for t in transactions if t['account_number'] in user_acc_nums]
    keyword = input('Search (transaction ID, type, or keyword): ').strip()
    results = search_transactions(user_txs, keyword)
    if not results:
        print('No matching transactions found.')
        return
    print(f'Found {len(results)} result(s):')
    for t in results:
        print(
            f'  [{t.get("transaction_id", "N/A")}] '
            f'{t["date"]}  {t["type"].upper():<14}  '
            f'${float(t["amount"]):.2f}  '
            f'{t.get("description", "")}'
        )


def reports_menu(username):
    while True:
        print('\n=== Reports & Visualization ===')
        print('1. Generate account report')
        print('2. Plot balance history')
        print('3. Export transactions to TXT')
        print('4. Back')
        try:
            choice = int(input('> '))
            if choice == 1:
                generate_report(username)
            elif choice == 2:
                plot_balance_history(username)
            elif choice == 3:
                export_to_txt(username)
            elif choice == 4:
                break
            else:
                print('Invalid option.')
        except ValueError:
            print('Please enter a valid option.')


def _print_accounts(user_accounts):
    # Shared helper to avoid repeating the same account display loop
    # in every transaction function
    print('Your accounts:')
    for acc_num, acc in user_accounts.items():
        print(f'  {acc_num}  ({acc["type"].capitalize()})  ${acc["balance"]:.2f}')


# Only run the app when this file is executed directly.
# Importing main.py from another module won't accidentally start the program.
if __name__ == '__main__':
    username = print_login_menu()
    banking_menu(username)
