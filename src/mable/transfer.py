from dataclasses import dataclass
from decimal import Decimal

from mable.errors import InvalidTransferError
from mable.money import validate_money

from dataclasses import dataclass


@dataclass(frozen=True)
class Transfer:
    from_acc: str
    to_acc: str
    amount: Decimal

    def __post_init__(self) -> None:
        validate_money(self.amount, label="Transfer amount")
        if self.from_acc == self.to_acc:
            raise InvalidTransferError(
                f"You  cannot transfer from the same account"
            )