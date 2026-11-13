from decimal import Decimal
from pathlib import Path

import pytest

from mable.loader import load_accounts

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