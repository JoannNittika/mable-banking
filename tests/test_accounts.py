from decimal import Decimal

import pytest

from mable.account import Account
from mable.errors import InsufficientFundsError

def test_account_has_number_and_balance():
    account = Account("1111234522226789", Decimal("5000.00"))
    assert account.number == "1111234522226789"
    assert account.balance == Decimal("5000.00")

def test_increase_balance_after_deposit():
    account = Account("1111234522226789", Decimal("5000.00"))
    account.deposit(Decimal("55.55"))
    assert account.balance == Decimal("5055.55")

def test_decrease_balance_after_withdrawal():
    account = Account("1111234522226789", Decimal("5000.00"))
    account.withdraw(Decimal("55.55"))
    assert account.balance == Decimal("5000.00")

