class InsufficientFundsError(Exception):
    """raised when a withdrawal puts the account balance to below zero"""

class InvalidAmountError(ValueError):
    """Raised when an amount is not a positive Decimal."""

class InvalidAccountNumberError(ValueError):
    """Raised when an account number is not exactly 16 digits."""

class InvalidTransferError(ValueError):
    """Raised when a transfer is malformed, e.g. to the same account."""

class AccountNotFoundError(KeyError):
    """Raised when a transfer names an account the bank doesn't hold."""

class DuplicateAccountError(ValueError):
    """Raised when the same account number is loaded into a bank twice."""