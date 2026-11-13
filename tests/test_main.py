from pathlib import Path

from mable.__main__ import main

DATA = Path(__file__).parent.parent / "data"
ACCOUNTS = DATA / "mable_account_balances.csv"
TRANSFERS = DATA / "mable_transactions.csv"


def test_main_prints_final_balances(capsys):
    main(ACCOUNTS, TRANSFERS)
    out = capsys.readouterr().out

    assert "Final balances" in out
    for balance in ["4,820.50", "9,974.40", "1,550.00", "1,725.60", "48,679.50"]:
        assert balance in out


def test_main_prints_completed_transfers(capsys):
    main(ACCOUNTS, TRANSFERS)
    out = capsys.readouterr().out

    assert "Completed transfers" in out
    assert "4 completed, 0 failed" in out


def test_main_prints_failed_transfers(tmp_path, capsys):
    accounts = tmp_path / "accounts.csv"
    accounts.write_text(f"{'1' * 16},10.00\n{'2' * 16},0.00\n")
    transfers = tmp_path / "transfers.csv"
    transfers.write_text(f"{'1' * 16},{'2' * 16},50.00\n")

    main(accounts, transfers)
    out = capsys.readouterr().out

    assert "Failed transfers" in out
    assert "0 completed, 1 failed" in out