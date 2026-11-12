class InsufficientFundsError(Exception):
    """raised when a withdrawal puts the account balance to below zero"""

class InvalidAmountError(ValueError):
    """Raised when an amount is not a positive Decimal."""