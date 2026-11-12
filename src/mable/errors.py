class InsufficientFundsError(Exception):
    """raised when a withdrawal puts the account balance to below zero"""

class InvalidAmountError(ValueError):
    """Raised when an amount is not a positive Decimal."""

class InvalidAccountNumberError(ValueError):
    """Raised when an account number is not exactly 16 digits."""