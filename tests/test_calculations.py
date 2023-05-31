# Testing file and testing function must follow test_ naming convention
import pytest
from app.calculations import add, BankAccount


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.fixture
def zero_bank_account():
    return BankAccount()

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

@pytest.mark.parametrize("deposit, withdrew, expected",[
                         (100, 50, 50),
                         (1200, 1300, -100)])
def test_bank_trans(zero_bank_account, deposit, withdrew, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

