from decimal import Decimal

class Account:
    def __init__(self, act_num: str, balance: Decimal) -> None:
        raise NotImplementedError

    def deposit(self, amount: Decimal)-> None:
        raise NotImplementedError

    def withdraw(self, amount: Decimal) -> None:
        raise NotImplementedError