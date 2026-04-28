class Account:
    def __init__(self, account_number, balance, owner):
        # Normalize types early: JSON loads all dict keys as strings and
        # balances may arrive as int — keeping them consistent prevents
        # subtle comparison bugs throughout the app
        self.account_number = str(account_number)
        self.balance = float(balance)
        self.owner = owner

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def __str__(self):
        return f'{self.account_number} | {self.owner} | ${self.balance:.2f}'


# CheckingAccount inherits all behaviour from Account with no extra rules
class CheckingAccount(Account):
    def __init__(self, account_number, balance, owner):
        super().__init__(account_number, balance, owner)


class SavingsAccount(Account):
    def __init__(self, account_number, balance, owner, interest_rate=0.02):
        super().__init__(account_number, balance, owner)
        self.interest_rate = interest_rate

    def apply_interest(self):
        # Single-period simple interest application
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest

    def compound_interest(self, periods):
        # Recursive implementation: apply one period of interest, then
        # call itself with one fewer period remaining.
        # Base case: no periods left, return the final balance.
        if periods == 0:
            return self.balance
        self.balance += self.balance * self.interest_rate
        return self.compound_interest(periods - 1)
