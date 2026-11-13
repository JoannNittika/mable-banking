from decimal import Decimal

from mable.account import Account
from mable.errors import AccountNotFoundError, DuplicateAccountError, InsufficientFundsError
from mable.transfer import Transfer


class Bank:
    def __init__(self, accounts: list[Account]) -> None:
        self._accounts: dict[str, Account] = {}
        for account in accounts:
            self._add_account(account)
        self.completed_transfers: list[Transfer] = []
        self.failed_transfers: list[tuple[Transfer, Exception]] = []

    def _add_account(self, account: Account) -> None:
        if account.act_num in self._accounts:
            raise DuplicateAccountError(f"Account {account.act_num} appears more than once")
        self._accounts[account.act_num] = account

    # Mainly used in testing
    def balance_of(self, number: str) -> Decimal:
        return self._get_account(number).balance

    # Moves money for one transfer, all or nothing; raises on missing account or low funds.
    def apply(self, transfer: Transfer) -> None:
        src = self._get_account(transfer.from_acc)
        target = self._get_account(transfer.to_acc)
        # Raises error when failed
        src.withdraw(transfer.amount)
        target.deposit(transfer.amount)
        # Only successful transactions with no errors raised is added to the list
        self.completed_transfers.append(transfer)

    # Applies transfers in order; failures are recorded with their error and don't stop the batch.
    def process(self, transfers: list[Transfer]) -> list[tuple[Transfer, Exception]] | None:
        failures: list[tuple[Transfer, Exception]] = []
        for transfer in transfers:
            try:
                self.apply(transfer)
            except (AccountNotFoundError, InsufficientFundsError) as error:
                failures.append((transfer, error))
        self.failed_transfers.extend(failures)
        return failures

    def _get_account(self, act_num: str) -> Account:
        try:
            return self._accounts[act_num]
        except KeyError:
            # Raises a clear banking error instead of a raw KeyError
            raise AccountNotFoundError(act_num) from None
