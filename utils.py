from accounts import CheckingAccount, SavingsAccount


def get_valid_amount():
    # Loop until the user enters a positive number, rejecting non-numeric input
    while True:
        try:
            amount = float(input('Enter amount: $'))
            if amount <= 0:
                print('Amount must be greater than 0.')
                continue
            return amount
        except ValueError:
            print('Please enter a valid number.')


def get_user_accounts(accounts, username):
    # Filter the full accounts dict down to only the accounts owned by this user
    return {acc_num: acc for acc_num, acc in accounts.items() if acc['owner'] == username}


def account_to_object(acc_num, acc_dict):
    # Reconstruct the correct Account subclass from a JSON dictionary so that
    # class methods (deposit, withdraw, compound_interest) can be called on it
    if acc_dict['type'] == 'checking':
        return CheckingAccount(acc_num, acc_dict['balance'], acc_dict['owner'])
    return SavingsAccount(acc_num, acc_dict['balance'], acc_dict['owner'], acc_dict.get('interest_rate', 0.02))
