from pathlib import Path

from mable.__main__ import main

DATA = Path(__file__).parent.parent / "data"
ACCOUNTS = DATA / "mable_account_balances.csv"
TRANSFERS = DATA / "mable_transactions.csv"


def test_main_prints_final_balances(capsys):
    main(ACCOUNTS, TRANSFERS)
    out = capsys.readouterr().out

    assert "Final balances:" in out
    for balance in ["4820.50", "9974.40", "1550.00", "1725.60", "48679.50"]:
        assert balance in out


def test_main_prints_completed_transfers(capsys):
    main(ACCOUNTS, TRANSFERS)
    out = capsys.readouterr().out

    assert "Completed:" in out
    assert out.count("Transfer(") == 4


def test_main_prints_failed_transfers(tmp_path, capsys):
    accounts = tmp_path / "accounts.csv"
    accounts.write_text(f"{'1' * 16},10.00\n{'2' * 16},0.00\n")
    transfers = tmp_path / "transfers.csv"
    transfers.write_text(f"{'1' * 16},{'2' * 16},50.00\n")

    main(accounts, transfers)
    out = capsys.readouterr().out

    assert "Failed:" in out
    assert "->" in out