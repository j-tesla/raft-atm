import pathlib
import sys

from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from data import Data

actions = ['withdraw', 'deposit', 'balance', 'transfer', 'quit']

_data = None


class ActionValidator(Validator):
    def validate(self, document):
        text = document.text
        if text not in actions:
            raise ValidationError(
                message='Invalid action',
                cursor_position=len(text))


class NumberValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text.isdigit():
            raise ValidationError(
                message='Invalid number',
                cursor_position=len(text))


def withdraw():
    account = prompt('Account: ')
    amount = prompt('Amount: ', validator=NumberValidator())
    if _data.withdraw(account, int(amount)):
        print('Withdraw successful')
    else:
        print('Withdraw failed')


def deposit():
    account = prompt('Account: ')
    amount = prompt('Amount: ', validator=NumberValidator())
    _data.deposit(account, int(amount))
    print('Deposit successful')


def balance():
    account = prompt('Account: ')
    print('Balance:', _data.get_balance(account))


def transfer():
    from_account = prompt('From account: ')
    to_account = prompt('To account: ')
    amount = prompt('Amount: ', validator=NumberValidator())
    if _data.transfer(from_account, to_account, int(amount)):
        print('Transfer successful')
    else:
        print('Transfer failed')


def menu():
    action = prompt('>', completer=WordCompleter(actions), validator=ActionValidator())
    if action == 'withdraw':
        withdraw()
    elif action == 'deposit':
        deposit()
    elif action == 'balance':
        balance()
    elif action == 'transfer':
        transfer()
    elif action == 'quit':
        quit()


def main():
    if len(sys.argv) < 2:
        print('Usage: %s selfHost:port partner1Host:port partner2Host:port ...')
        sys.exit(-1)

    if not pathlib.Path('.journals').exists():
        pathlib.Path('.journals').mkdir()

    self_address = sys.argv[1]
    other_addresses = sys.argv[2:]

    if self_address == 'readonly':
        self_address = None
    global _data
    _data = Data(self_address, other_addresses)

    while True:
        menu()


if __name__ == '__main__':
    main()
