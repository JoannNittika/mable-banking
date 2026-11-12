from decimal import Decimal
from idlelib import statusbar

from mable.errors import InsufficientFundsError, InvalidAmountError

class Account:
    def __init__(self, act_num: str, balance: Decimal) -> None:
        self.act_num = act_num
        self.balance = balance

    def deposit(self, amount: Decimal)-> None:
        self.validate_amount(amount)
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        self.validate_amount(amount)
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Account {self.number} has {self.balance}, cannot withdraw {amount}"
            )
        self.balance -= amount

    @staticmethod
    def validate_amount(amount: Decimal)-> None:
        if not isinstance(amount, Decimal) or amount <=0:
            raise InvalidAmountError(f"{amount} is invalid. Amount must be a positive Decimal")
