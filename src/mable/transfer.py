from dataclasses import dataclass
from decimal import Decimal

from mable.errors import InvalidAmountError, InvalidTransferError

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Transfer:
    from_account: str
    to_account: str
    amount: Decimal

    def __post_init__(self) -> None:
        raise NotImplementedError