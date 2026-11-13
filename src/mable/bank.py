from decimal import Decimal

from mable.account import Account
from mable.transfer import Transfer
from mable.errors import AccountNotFoundError, DuplicateAccountError, InsufficientFundsError


class Bank:
    def __init__(self, accounts: list[Account]) -> None:
        self.accounts: dict[str, Account] = {}
        for account in accounts:
            self._add_account(account)
        self.completed_transfers: list[Transfer] = []

    def _add_account(self, account: Account) -> None:
        if account.act_num in self.accounts:
            raise DuplicateAccountError(f"Account {account.act_num} appears more than once")
        self.accounts[account.act_num] = account

    #Mainly used in testing
    def balance_of(self, number: str) -> Decimal:
            return self.get_account(number).balance

    def apply(self, transfer: Transfer) -> None:
        src = self.get_account(transfer.from_acc)
        target = self.get_account(transfer.to_acc)
        #Raises error when failed
        src.withdraw(transfer.amount)
        target.deposit(transfer.amount)
        #Only successful transactions with no errors raised is added to the list
        self.completed_transfers.append(transfer)

    def process(self, transfers: list[Transfer]) -> list[tuple[Transfer, Exception]] | None:
        failures: list[tuple[Transfer, Exception]] = []
        for transfer in transfers:
            try:
                self.apply(transfer)
            except (AccountNotFoundError, InsufficientFundsError) as error:
                failures.append((transfer, error))
        return failures

    def get_account(self, act_num: str)-> Account:
        try:
            return self.accounts[act_num]
        except:
            #Raises a clear banking error instead of a raw KeyError
            raise AccountNotFoundError(act_num) from None