from decimal import Decimal

import pytest

from mable.errors import InvalidAmountError
from mable.money import validate_money


@pytest.mark.parametrize("good", [Decimal("1"), Decimal("1.5"), Decimal("1.50"), Decimal("1.230"), Decimal("0.01")])
def test_accepts_amounts_with_at_most_two_decimal_places(good):
    validate_money(good)


@pytest.mark.parametrize("bad", [Decimal("1.234"), Decimal("0.001"), Decimal("100.005")])
def test_rejects_amounts_with_more_than_two_decimal_places(bad):
    with pytest.raises(InvalidAmountError, match="2 decimal places"):
        validate_money(bad)


@pytest.mark.parametrize("bad", [Decimal("NaN"), Decimal("sNaN"), Decimal("Infinity"), Decimal("-Infinity")])
def test_rejects_non_finite_amounts(bad):
    with pytest.raises(InvalidAmountError, match="finite"):
        validate_money(bad)


def test_zero_only_allowed_when_requested():
    validate_money(Decimal("0"), allow_zero=True)
    with pytest.raises(InvalidAmountError):
        validate_money(Decimal("0"))


def test_rejects_amount_too_large_to_express_in_cents():
    with pytest.raises(InvalidAmountError):
        validate_money(Decimal("1E+30"))