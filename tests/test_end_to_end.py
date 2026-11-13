from decimal import Decimal
from pathlib import Path

from mable.bank import Bank
from mable.errors import AccountNotFoundError, InsufficientFundsError
from mable.loader import load_accounts, load_transfers

DATA = Path(__file__).parent.parent / "data"
A = "1111234522226789"
B = "1111234522221234"


def run(accounts_path, transfers_path):
    accounts = load_accounts(accounts_path)
    bank = Bank(accounts)
    bank.process(load_transfers(transfers_path))
    return accounts, bank


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text)
    return path


def test_sample_files_give_expected_final_balances():
    accounts, bank = run(DATA / "mable_account_balances.csv", DATA / "mable_transactions.csv")

    # Same order as mable_account_balances.csv
    assert [a.balance for a in accounts] == [
        Decimal("4820.50"),
        Decimal("9974.40"),
        Decimal("1550.00"),
        Decimal("1725.60"),
        Decimal("48679.50"),
    ]
    assert len(bank.completed_transfers) == 4
    assert bank.failed_transfers == []


def test_sample_files_keep_total_money_the_same():
    before = sum(a.balance for a in load_accounts(DATA / "mable_account_balances.csv"))
    accounts, _ = run(DATA / "mable_account_balances.csv", DATA / "mable_transactions.csv")

    assert before == Decimal("66750.00")
    assert sum(a.balance for a in accounts) == before


def test_failed_transfers_are_recorded_and_the_rest_still_run(tmp_path):
    accounts_csv = write(tmp_path, "accounts.csv", f"{A},100.00\n{B},50.00\n")
    transfers_csv = write(tmp_path, "transfers.csv",
                          f"{B},{A},500.00\n"            # not enough money
                          f"{A},{'9' * 16},1.00\n"       # unknown account
                          f"{A},{B},30.00\n")            # fine
    accounts, bank = run(accounts_csv, transfers_csv)

    assert [a.balance for a in accounts] == [Decimal("70.00"), Decimal("80.00")]
    assert len(bank.completed_transfers) == 1
    assert [type(error) for _, error in bank.failed_transfers] == [
        InsufficientFundsError,
        AccountNotFoundError,
    ]


def test_transfers_run_in_file_order(tmp_path):
    # B can only pay A back after receiving money from A first
    accounts_csv = write(tmp_path, "accounts.csv", f"{A},100.00\n{B},0.00\n")
    transfers_csv = write(tmp_path, "transfers.csv", f"{A},{B},60.00\n{B},{A},60.00\n")
    accounts, bank = run(accounts_csv, transfers_csv)

    assert [a.balance for a in accounts] == [Decimal("100.00"), Decimal("0.00")]
    assert bank.failed_transfers == []


def test_spending_the_exact_balance_is_allowed(tmp_path):
    accounts_csv = write(tmp_path, "accounts.csv", f"{A},25.60\n{B},0.00\n")
    transfers_csv = write(tmp_path, "transfers.csv", f"{A},{B},25.60\n")
    accounts, _ = run(accounts_csv, transfers_csv)

    assert [a.balance for a in accounts] == [Decimal("0.00"), Decimal("25.60")]