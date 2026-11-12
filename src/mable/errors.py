class InsufficientFundsError(Exception):
    """raised when a withdrawal puts the account balance to below zero"""