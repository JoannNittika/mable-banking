from decimal import Decimal

from mable.errors import InsufficientFundsError, InvalidAccountNumberError
from mable.money import validate_money


class Account:
    NUMBER_LENGTH = 16

    def __init__(self, act_num: str, balance: Decimal) -> None:
        self._validate_account_number(act_num)
        self._validate_opening_balance(balance)
        self.act_num = act_num
        self.balance = balance

    def deposit(self, amount: Decimal) -> None:
        self._validate_amount(amount)
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        self._validate_amount(amount)
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Account {self.act_num} has {self.balance}, cannot withdraw {amount}"
            )
        self.balance -= amount

    #private methods
    @classmethod
    def _validate_account_number(cls, act_num: str) -> None:
        if (
            not isinstance(act_num, str)
            or len(act_num) != cls.NUMBER_LENGTH
            or not act_num.isdigit()
        ):
            raise InvalidAccountNumberError(
                f"Account number must be {cls.NUMBER_LENGTH} digits, got {act_num!r}"
            )

    @staticmethod
    def _validate_opening_balance(balance: Decimal) -> None:
        validate_money(balance, allow_zero=True, label="Opening balance")

    @staticmethod
    def _validate_amount(amount: Decimal) -> None:
        validate_money(amount)
