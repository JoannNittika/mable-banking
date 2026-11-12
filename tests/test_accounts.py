from decimal import Decimal

import pytest

from mable.account import Account
from mable.errors import InsufficientFundsError, InvalidAmountError

def test_account_has_number_and_balance():
    account = Account("1111234522226789", Decimal("5000.00"))
    assert account.act_num == "1111234522226789"
    assert account.balance == Decimal("5000.00")

def test_increase_balance_after_deposit():
    account = Account("1111234522226789", Decimal("5000.00"))
    account.deposit(Decimal("55.55"))
    assert account.balance == Decimal("5055.55")

def test_decrease_balance_after_withdrawal():
    account = Account("1111234522226789", Decimal("5055.55"))
    account.withdraw(Decimal("55.55"))
    assert account.balance == Decimal("5000.00")

@pytest.mark.parametrize("bad", [Decimal("0"), Decimal("-10.00"), "50", 50.0, None])
def test_deposit_rejects_invalid_amounts(bad):
    account = Account("1111234522226789", Decimal("100.00"))
    with pytest.raises(InvalidAmountError):
        account.deposit(bad)
    assert account.balance == Decimal("100.00")


@pytest.mark.parametrize("bad", [Decimal("0"), Decimal("-10.00"), "50", 50.0, None])
def test_withdraw_rejects_invalid_amounts(bad):
    account = Account("1111234522226789", Decimal("100.00"))
    with pytest.raises(InvalidAmountError):
        account.withdraw(bad)
    assert account.balance == Decimal("100.00")

