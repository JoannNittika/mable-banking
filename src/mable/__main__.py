from pathlib import Path

from mable.bank import Bank
from mable.loader import load_accounts, load_transfers


def main(
    accounts_path: str | Path = "data/mable_account_balances.csv",
    transfers_path: str | Path = "data/mable_transactions.csv",
) -> None:
    accounts = load_accounts(accounts_path)
    bank = Bank(accounts)
    bank.process(load_transfers(transfers_path))

    print("Completed:")
    for transfer in bank.completed_transfers:
        print(" ", transfer)
    print("Failed:")
    for transfer, error in bank.failed_transfers:
        print(" ", transfer, "->", error)
    print("Final balances:")
    for account in accounts:
        print(f"  {account.act_num}: {account.balance:.2f}")


if __name__ == "__main__": # pragma: no cover
    main()