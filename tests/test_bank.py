from decimal import Decimal

import pytest

from mable.account import Account
from mable.bank import Bank
from mable.errors import AccountNotFoundError, InsufficientFundsError
from mable.transfer import Transfer

A = "1234567890123456"
B = "6543210123456789"


@pytest.fixture
def bank():
    return Bank([Account(A, Decimal("100.00")), Account(B, Decimal("50.00"))])


def test_apply_transfers_money(bank):
    bank.apply(Transfer(A, B, Decimal("30.00")))
    assert bank.balance_of(A) == Decimal("70.00")
    assert bank.balance_of(B) == Decimal("80.00")


def test_insufficient_funds_leaves_balances_untouched(bank):
    with pytest.raises(InsufficientFundsError):
        bank.apply(Transfer(B, A, Decimal("50.01")))
    assert bank.balance_of(A) == Decimal("100.00")
    assert bank.balance_of(B) == Decimal("50.00")


def test_unknown_account_raises(bank):
    with pytest.raises(AccountNotFoundError):
        bank.apply(Transfer(A, "9999999999999999", Decimal("1.00")))
    assert bank.balance_of(A) == Decimal("100.00")


def test_process_applies_in_order_and_collects_failures(bank):
    bad = Transfer(B, A, Decimal("500.00"))
    failures = bank.process([Transfer(A, B, Decimal("10.00")), bad])
    assert bank.balance_of(A) == Decimal("90.00")
    assert bank.balance_of(B) == Decimal("60.00")
    assert len(failures) == 1
    assert failures[0][0] == bad
    assert isinstance(failures[0][1], InsufficientFundsError)