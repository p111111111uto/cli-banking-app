import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from storage import load_accounts, load_transactions
from utils import get_user_accounts


def plot_balance_history(username):
    accounts = load_accounts()
    user_accounts = get_user_accounts(accounts, username)
    transactions = load_transactions()
    user_acc_nums = set(user_accounts.keys())
    user_txs = [t for t in transactions if t['account_number'] in user_acc_nums]

    if not user_txs:
        print('No transaction data to plot.')
        return

    df = pd.DataFrame(user_txs)
    df['amount'] = pd.to_numeric(df['amount'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')   # chronological order required for cumsum below

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'Balance History — {username}', fontsize=14)

    # --- Chart 1: running balance per account ---
    ax1 = axes[0]
    for acc_num in user_acc_nums:
        acc_df = df[df['account_number'] == acc_num].copy()
        if acc_df.empty:
            continue

        # Deposits and incoming transfers increase the balance (positive);
        # withdrawals and outgoing transfers decrease it (negative)
        acc_df['signed'] = acc_df.apply(
            lambda r: r['amount'] if r['type'] in ('deposit', 'transfer_in') else -r['amount'],
            axis=1
        )
        # cumsum() gives the running total after each transaction
        acc_df['running_balance'] = acc_df['signed'].cumsum()
        ax1.plot(acc_df['date'], acc_df['running_balance'], marker='o', label=acc_num)

    ax1.set_title('Running Balance Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Balance ($)')
    ax1.legend()
    ax1.grid(True)

    # --- Chart 2: total transaction volume per calendar month ---
    ax2 = axes[1]
    df['month'] = df['date'].dt.to_period('M').astype(str)  # e.g. "2026-04"
    monthly = df.groupby('month')['amount'].sum().reset_index()
    months = monthly['month'].values
    amounts = monthly['amount'].values
    # np.arange gives evenly-spaced integer positions for the bar chart ticks
    x = np.arange(len(months))
    ax2.bar(x, amounts, color='steelblue')
    ax2.set_xticks(x)
    ax2.set_xticklabels(months, rotation=45, ha='right')
    ax2.set_title('Monthly Transaction Volume')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Total Amount ($)')
    ax2.grid(axis='y')

    plt.tight_layout()
    plt.show()
