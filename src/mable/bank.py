from mable.account import Account
from mable.transfer import Transfer


class Bank:
    def __init__(self, accounts: list[Account]) -> None:
        raise NotImplementedError

    def balance_of(self, number: str):
        raise NotImplementedError

    def apply(self, transfer: Transfer) -> None:
        raise NotImplementedError

    def process(self, transfers: list[Transfer]) -> list[tuple[Transfer, Exception]]:
        raise NotImplementedError