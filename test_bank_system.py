import pytest
import datetime
from bank_system import bank_accounts, trx_perform, trx_create, name_by_get


@pytest.fixture
def setup_accounts():
    # Reset bank accounts to a known state before each test
    global bank_accounts
    bank_accounts = {
        1001: {
            "first_name": "Alice",
            "last_name": "Smith",
            "id_number": "123456789",
            "balance": 2500.50,
            "transactions_to_execute": [],
            "transaction_history": []
        },
        1002: {
            "first_name": "Bob",
            "last_name": "Johnson",
            "id_number": "987654321",
            "balance": 3900.75,
            "transactions_to_execute": [],
            "transaction_history": []
        }
    }
    return bank_accounts


def test_trx_perform_empty_transactions(setup_accounts):
    trx_create(bank_accounts, 1001, 1002, 100.00)
    trx_perform(bank_accounts, 1001)
    assert len(bank_accounts[1001]["transactions_to_execute"]) == 0


def test_trx_perform_history(setup_accounts):
    trx_create(bank_accounts, 1001, 1002, 100.00)
    trx_perform(bank_accounts, 1001)
    assert len(bank_accounts[1001]["transaction_history"]) > 0
    assert len(bank_accounts[1002]["transaction_history"]) > 0


def test_trx_perform_balance_source(setup_accounts):
    # Set up and perform transactions
    trx_create(bank_accounts, 1001, 1002, 100.00)
    trx_perform(bank_accounts, 1001)
    assert bank_accounts[1001]["balance"] == 2500.50 - 100.00


def test_trx_perform_balance_target(setup_accounts):
    # Set up and perform transactions
    trx_create(bank_accounts, 1001, 1002, 100.00)
    trx_perform(bank_accounts, 1001)
    assert bank_accounts[1002]["balance"] == 3900.75 + 100.00


def test_trx_create(setup_accounts, monkeypatch):
    # Simulate the current time
    monkeypatch.setattr('bank_system.current_time', lambda: '2024-09-08 10:00:00')

    # Create a transaction
    trx_create(bank_accounts, 1001, 1002, 50.00)
    assert len(bank_accounts[1001]["transactions_to_execute"]) == 1
    transaction = bank_accounts[1001]["transactions_to_execute"][0]
    assert transaction[1] == 1001
    assert transaction[2] == 1002
    assert transaction[3] == 50.00
    assert transaction[0] == '2024-09-08 10:00:00'


def test_name_by_get(setup_accounts):
    # Add accounts with the name 'bob'
    bank_accounts[1003] = {
        "first_name": "Bob",
        "last_name": "Davis",
        "id_number": "555555555",
        "balance": 1000.00,
        "transactions_to_execute": [],
        "transaction_history": []
    }

    result = name_by_get(bank_accounts, 'bo')
    assert len(result) == 2
    assert any(account["first_name"] == "Bob" for account in result)
