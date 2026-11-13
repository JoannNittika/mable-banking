# Mable Back-End Coding Test – Bank Transfers

## What the program does
The program loads a list of bank accounts and their opening balances from a CSV file. It then reads a list of transfers from a second CSV file and runs them in file order.

- Each account has a 16-digit account number and a balance. A balance can never go negative.
- A transfer moves money from one account to another. A transfer either fully succeeds or leaves both balances untouched.
- A transfer that fails (not enough funds, or an unknown account) is recorded with the reason it failed, and processing continues with the next transfer.
- At the end, the program prints the completed transfers, the failed transfers, and every account's final balance.

### Project layout
```
src/mable/
  account.py    Account: holds a balance, withdraw / deposit
  transfer.py   Transfer: immutable record of one transfer
  bank.py       Bank: holds accounts, applies and processes transfers
  money.py      Shared validation rules for money amounts
  loader.py     Reads the account and transfer CSV files
  errors.py     Custom exceptions
  __main__.py   Entry point (python -m mable)
tests/          Unit tests for each module, plus end-to-end tests
data/           Sample input CSV files
```

## Setup and running
Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync                      # create the virtual env and install dependencies
uv run python -m mable       # run against the files in data/
uv run pytest                # run all tests
uv run pytest -v             # verbose test output
```

Run the commands from the project root, the folder that contains `data/`.

### Input format
- `data/mable_account_balances.csv`: `account_number,balance`
- `data/mable_transactions.csv`: `from_account,to_account,amount`

The files have no header row.

## Assumptions
- **Money:** Amounts are stored as `Decimal`, never as `float`, to avoid rounding errors.
- **Decimal places:** Amounts must have at most 2 decimal places. Anything with more is rejected rather than rounded, because a bank should never quietly change the money it was given. A value like `1.230` is accepted because it's still a whole number of cents.
- **Invalid amounts:** `NaN`, `Infinity` and negative amounts are rejected.
- **Zero:** A zero amount is allowed for an opening balance but not for a transfer.
- **Account numbers:** Account numbers are exactly 16 digits and are stored as strings, so leading zeros are kept.
- **Same account:** A transfer from an account to itself is invalid.
- **Duplicate accounts:** The same account number appearing twice in the balances file raises an error. It does not overwrite the first entry.
- **Bad rows:** A malformed row stops loading with an error. This covers a wrong number of columns, an amount that isn't a number, and an invalid account number. Bad input data is a problem with the file, so it is reported rather than skipped.
- **Order:** Transfers run in the order they appear in the file.
- **Failed transfers:** A failed transfer (insufficient funds or unknown account) does not stop the batch. It is recorded in `Bank.failed_transfers` together with its error.
- **Blank lines and spaces:** Blank lines and surrounding spaces in the CSV files are ignored.

## How I used TDD
I built the project in red, green, refactor cycles:

1. **Red:** write a small failing test that describes one behaviour, for example "a withdrawal larger than the balance raises `InsufficientFundsError` and leaves the balance unchanged".
2. **Green:** write the minimum code to make that test pass.
3. **Refactor:** tidy the code while keeping every test green. For example, I moved the money checks shared by `Account` and `Transfer` into `money.py`, and I pulled the duplicated CSV-reading code in `loader.py` into one helper.

The order of work was:
1. `Account`
2. `Transfer`
3. `Bank`, applying a single transfer
4. `Bank`, processing a batch of transfers
5. The CSV loader
6. Storing failed transfers
7. End-to-end tests against the sample data

The end-to-end tests check the expected final balances and that the total money (66,750.00) is the same before and after.

## AI declaration
I used an AI assistant (Claude) during this test to help with:

- **Debugging:** reading failing test output and tracking down causes, such as a failed transfer being recorded twice, and a module import error caused by the package not being installed.
- **Understanding libraries:** Python's `decimal`, `csv`, `dataclasses`, pytest fixtures (`tmp_path`), `parametrize`, and `uv` project setup.
- **Writing extra test cases:** edge cases for the CSV loader, and end-to-end tests.
- **Code review:** analysing the project to find testing gaps and coding-standard issues, such as an unused import, a bare `except:`, missing NaN and Infinity checks, missing decimal-place validation, and duplicate accounts being silently overwritten.

I reviewed, understood and tested all the AI-suggested code myself before including it. The design decisions and the final code are my own.
