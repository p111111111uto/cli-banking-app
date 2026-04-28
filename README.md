# Python CLI Banking Application

A command-line banking application built with Python for COP1047C.

## How to Run

1. Install dependencies:
   ```
   pip install matplotlib pandas numpy
   ```
2. Run the application:
   ```
   python main.py
   ```

## Features

- **User Management** — Register and login with SHA-256 hashed passwords
- **Account Types** — Create Checking or Savings accounts with random 8-digit account numbers
- **Deposit / Withdraw** — Add or remove funds with balance validation
- **Transfer** — Move funds between any two accounts
- **View Balances** — See all your accounts and a running total
- **Transaction History** — View all transactions, sorted by date or amount
- **Compound Interest** — Recursively apply compound interest to savings accounts over N periods
- **Search** — Search transactions by ID, type, or keyword (linear search)
- **Sorting** — Bubble sort applied to transaction lists by date or amount
- **Reports** — Summary report showing totals for deposits, withdrawals, and transfers
- **Export** — Export transaction history to a TXT file
- **Charts** — Plot running balance over time and monthly transaction volume (matplotlib + pandas + numpy)

## Project Structure

```
cli_banking_project_max_martinez/
├── main.py           # Entry point, all menus
├── auth.py           # Registration and login
├── accounts.py       # Account, CheckingAccount, SavingsAccount classes
├── transactions.py   # Transaction class, deposit/withdraw/transfer functions
├── storage.py        # JSON and CSV file I/O
├── reports.py        # Sorting, searching, report generation, TXT export
├── plotting.py       # Matplotlib/pandas/numpy charts
├── utils.py          # Shared helper functions
└── data/
    ├── users.json
    ├── accounts.json
    ├── transactions.csv
    └── report.txt    # Generated on export
```

## Python Concepts Used

| Concept | Where |
|---|---|
| Variables & Expressions | Balances, account numbers |
| Types | int, float, str, bool throughout |
| Branching & Loops | All menu logic |
| Functions | Every action is a function |
| Strings | Input handling, formatted output |
| Exceptions | All user input wrapped in try/except |
| Lists & Dictionaries | Transaction lists, account dicts |
| Classes | Account, CheckingAccount, SavingsAccount, Transaction |
| Inheritance | CheckingAccount and SavingsAccount extend Account |
| Modules | auth, transactions, reports, plotting, storage, utils |
| Files | JSON (users, accounts), CSV (transactions), TXT (export) |
| Plotting | matplotlib bar chart + line chart, pandas, numpy |
| Recursion | `compound_interest(periods)` in SavingsAccount |
| Sorting | Bubble sort in `reports.sort_transactions()` |
| Searching | Linear search in `reports.search_transactions()` |

## Challenges & Reflections

- JSON stores all dictionary keys as strings, so account numbers entered as integers had to be normalized to strings consistently across all modules.
- Reconstructing a running balance from a flat transaction log required tracking signed amounts per account, which was a good use of pandas.
- Implementing recursive compound interest required careful thought about the base case to avoid infinite recursion.
