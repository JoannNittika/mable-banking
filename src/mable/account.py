from decimal import Decimal
from mable.errors import InsufficientFundsError

class Account:
    def __init__(self, act_num: str, balance: Decimal) -> None:
        self.act_num = act_num
        self.balance = balance

    def deposit(self, amount: Decimal)-> None:
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Account {self.number} has {self.balance}, cannot withdraw {amount}"
            )
        self.balance -= amount