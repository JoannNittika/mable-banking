"""Validation rules shared by every money amount in the system."""

from decimal import Decimal, InvalidOperation

from mable.errors import InvalidAmountError

CENT = Decimal("0.01")


def validate_money(amount: Decimal, *, allow_zero: bool = False, label: str = "Amount") -> None:
    """Raise InvalidAmountError unless amount is a finite Decimal with at most 2 decimal places.

    Zero is only allowed when allow_zero is True (e.g. an opening balance).
    Amounts with more than 2 decimal places are rejected rather than rounded,
    so the system never silently changes the money it was given.
    """
    if not isinstance(amount, Decimal) or not amount.is_finite():
        raise InvalidAmountError(f"{label} must be a finite Decimal, got {amount!r}")
    if amount < 0 or (amount == 0 and not allow_zero):
        minimum = ">= 0" if allow_zero else "> 0"
        raise InvalidAmountError(f"{label} must be {minimum}, got {amount}")
    if not _has_at_most_two_decimal_places(amount):
        raise InvalidAmountError(f"{label} must have at most 2 decimal places, got {amount}")


def _has_at_most_two_decimal_places(amount: Decimal) -> bool:
    try:
        return amount == amount.quantize(CENT)
    except InvalidOperation:
        # Too many digits to represent in cents at the current precision.
        return False
