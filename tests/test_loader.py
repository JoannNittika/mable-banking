from decimal import Decimal
from pathlib import Path

import pytest

from mable.loader import load_accounts, load_transfers

from mable.errors import InvalidAccountNumberError, InvalidAmountError, InvalidTransferError

DATA = Path(__file__).parent.parent / "data"
A = "1111234522226789"
B = "2222123433331212"


@pytest.fixture
def csv_file(tmp_path):
    """Write some CSV text to a temp file and return its path."""
    def write(text):
        path = tmp_path / "input.csv"
        path.write_text(text)
        return path
    return write


def test_load_accounts_reads_each_row(csv_file):
    accounts = load_accounts(csv_file(f"{A},5000.00\n{B},550.00\n"))

    assert [(a.act_num, a.balance) for a in accounts] == [
        (A, Decimal("5000.00")),
        (B, Decimal("550.00")),
    ]


def test_load_accounts_reads_the_sample_file():
    accounts = load_accounts(DATA / "mable_account_balances.csv")

    assert len(accounts) == 5
    assert accounts[0].act_num == A
    assert accounts[0].balance == Decimal("5000.00")

def test_load_transfers_keeps_file_order(csv_file):
    transfers = load_transfers(csv_file(f"{A},{B},500.00\n{B},{A},25.60\n"))
    assert [(t.from_acc, t.to_acc, t.amount) for t in transfers] == [
        (A, B, Decimal("500.00")),
        (B, A, Decimal("25.60")),
    ]


def test_load_transfers_reads_the_sample_file():
    transfers = load_transfers(DATA / "mable_transactions.csv")
    assert len(transfers) == 4
    assert transfers[-1].amount == Decimal("25.60")


def test_empty_file_loads_nothing(csv_file):
    assert load_accounts(csv_file("")) == []
    assert load_transfers(csv_file("")) == []


def test_blank_lines_and_spaces_are_ignored(csv_file):
    accounts = load_accounts(csv_file(f"\n {A} , 5000.00 \n\n"))
    assert [(a.act_num, a.balance) for a in accounts] == [(A, Decimal("5000.00"))]

@pytest.mark.parametrize("row, error", [
    (f"{A},abc", InvalidAmountError),            # not a number
    (f"{A},-1.00", InvalidAmountError),          # negative
    (f"{A},1.234", InvalidAmountError),          # 3 decimal places
    ("1234,100.00", InvalidAccountNumberError),  # not 16 digits
    (f"{A}", ValueError),                        # missing column
    (f"{A},100.00,extra", ValueError),           # extra column
])
def test_load_accounts_rejects_bad_rows(csv_file, row, error):
    with pytest.raises(error):
        load_accounts(csv_file(row))


@pytest.mark.parametrize("row, error", [
    (f"{A},{B},abc", InvalidAmountError),        # not a number
    (f"{A},{B},0", InvalidAmountError),          # zero
    (f"{A},{A},10.00", InvalidTransferError),    # same account
    (f"{A},{B}", ValueError),                    # missing column
])
def test_load_transfers_rejects_bad_rows(csv_file, row, error):
    with pytest.raises(error):
        load_transfers(csv_file(row))


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_accounts(tmp_path / "missing.csv")
