import csv
from decimal import Decimal, InvalidOperation

from mable.account import Account
from mable.errors import InvalidAmountError
from mable.transfer import Transfer



def load_accounts(path) -> list[Account]:
    return [Account(act_num, _to_decimal(balance)) for act_num, balance in _read_rows(path)]

def load_transfers(path) -> list[Transfer]:
    return [Transfer(source, target, _to_decimal(amount)) for source, target, amount in _read_rows(path)]


def _read_rows(path) -> list[list[str]]:
    """Read a CSV file, trimming spaces and skipping blank lines."""
    with open(path, newline="") as file:
        rows = [[cell.strip() for cell in row] for row in csv.reader(file)]
    return [row for row in rows if any(row)]


def _to_decimal(text: str) -> Decimal:
    try:
        return Decimal(text)
    except InvalidOperation:
        raise InvalidAmountError(f"{text!r} is not a number") from None