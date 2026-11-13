from pathlib import Path

from mable.bank import Bank
from mable.loader import load_accounts, load_transfers


def main(
    accounts_path: str | Path = "data/mable_account_balances.csv",
    transfers_path: str | Path = "data/mable_transactions.csv",
) -> None:
    try:
        accounts = load_accounts(accounts_path)
        bank = Bank(accounts)
        transfers = load_transfers(transfers_path)
    except (ValueError, LookupError) as error:
        print(f"Error: {error}")
        raise SystemExit(1) from None
    bank.process(transfers)

    done, failed = bank.completed_transfers, bank.failed_transfers
    print(f"Processed {len(done) + len(failed)} transfers: "
          f"{len(done)} completed, {len(failed)} failed\n")

    print("Completed transfers")
    for t in done:
        print(f"  {t}")

    if failed:
        print("\nFailed transfers")
        for transfer, error in bank.failed_transfers:
            print(f"  {transfer.from_acc} -> {transfer.to_acc} ${transfer.amount:,.2f}: {error}")

    print("\nFinal balances")
    print(f"  {'Account':<18}{'Balance':>14}")
    for a in accounts:
        print(f"  {a.act_num:<18}{a.balance:>14,.2f}")


if __name__ == "__main__": # pragma: no cover
    main()