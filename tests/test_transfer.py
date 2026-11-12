from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from mable.errors import InvalidAmountError, InvalidTransferError
from mable.transfer import Transfer

FROM = "1234567890123456"
TO = "6543210123456789"

def test_transfer_class():
    transfer = Transfer(FROM, TO, Decimal("100.00"))
    assert transfer.from_acc == FROM
    assert transfer.to_acc == TO
    assert transfer.amount == Decimal("100.00")

def test_transfer_is_immutable():
    transfer = Transfer(FROM, TO, Decimal("500.00"))
    with pytest.raises(FrozenInstanceError):
        setattr(transfer, "amount", Decimal("1.00"))

@pytest.mark.parametrize("bad", [Decimal("0"), Decimal("-5.00"), "500", 500.0, None])
def test_rejects_invalid_amount(bad):
    with pytest.raises(InvalidAmountError):
        Transfer(FROM, TO, bad)


def test_rejects_transfer_to_same_account():
    with pytest.raises(InvalidTransferError):
        Transfer(FROM, FROM, Decimal("10.00"))
