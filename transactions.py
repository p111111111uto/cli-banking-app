import uuid
from datetime import datetime
from storage import save_transaction


class Transaction:
    def __init__(self, account_number, transaction_type, amount, description=''):
        # uuid4 generates a random 128-bit ID; we take the first 8 characters
        # for a shorter, human-readable transaction ID (e.g. "A3F9C12B")
        self.transaction_id = str(uuid.uuid4())[:8].upper()
        self.account_number = str(account_number)
        self.type = transaction_type
        self.amount = amount
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.description = description

    def to_dict(self):
        # Returns a plain dictionary so the transaction can be written to CSV
        return {
            'transaction_id': self.transaction_id,
            'account_number': self.account_number,
            'type': self.type,
            'amount': self.amount,
            'date': self.date,
            'description': self.description,
        }

    def record(self):
        save_transaction(self.to_dict())


def deposit(account, amount, description='Deposit'):
    account.deposit(amount)
    t = Transaction(account.account_number, 'deposit', amount, description)
    t.record()
    return t


def withdraw(account, amount, description='Withdrawal'):
    account.withdraw(amount)
    t = Transaction(account.account_number, 'withdrawal', amount, description)
    t.record()
    return t


def transfer(from_account, to_account, amount):
    from_account.withdraw(amount)
    to_account.deposit(amount)
    # Two records are created so each account's own history stays accurate
    t_out = Transaction(from_account.account_number, 'transfer_out', amount, f'To {to_account.account_number}')
    t_out.record()
    t_in = Transaction(to_account.account_number, 'transfer_in', amount, f'From {from_account.account_number}')
    t_in.record()
