from dataclasses import dataclass
from decimal import Decimal

from mable.errors import InvalidAmountError, InvalidTransferError

from dataclasses import dataclass


@dataclass(frozen=True)
class Transfer:
    from_acc: str
    to_acc: str
    amount: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal) or self.amount <= 0:
            raise InvalidAmountError(
                f"Amount for transfer is {self.amount}. Amount must be positive, non-zero decimal value"
            )
        if self.from_acc == self.to_acc:
            raise InvalidTransferError(
                f"You  cannot transfer from the same account"
            )