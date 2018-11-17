from pprint import pprint  # noqa
import rlp
from rlp.sedes import (
    text,
)


class Header(rlp.Serializable):
    fields = (
        ('Type', text),
    )


class CreateAccountBody(rlp.Serializable):
    fields = (
        ('Target', text),
        ('Amount', text),
        ('Linked', text),
    )


class PaymentBody(rlp.Serializable):
    fields = (
        ('Target', text),
        ('Amount', text),
    )


class Operation(rlp.Serializable):
    fields = (
        ('H', Header),
        ('B', PaymentBody),
    )

    @classmethod
    def from_dict(cls, d):
        if d['H']['type'] == 'create-account':
            return CreateAccount.from_dict(d)
        elif d['H']['type'] == 'payment':
            return Payment.from_dict(d)
        else:
            raise Exception('unknown operation: %s' % d)


class CreateAccount(Operation):
    fields = (
        ('H', Header),
        ('B', CreateAccountBody),
    )

    def to_dict(self):
        o = self.as_dict()
        h = o['H'].as_dict()
        b = o['B'].as_dict()

        return dict(
            H=dict(
                type=h['Type'],
            ),
            B=dict(
                amount=b['Amount'],
                target=b['Target'],
                linked=b.get('Linked', ''),
            ),
        )

    @classmethod
    def from_dict(cls, d):
        assert d['H']['type'] == 'create-account'

        return cls(
            H=Header(Type='create-account'),
            B=CreateAccountBody(Target=d['B']['target'], Amount=d['B']['amount'], Linked=d['B'].get('linked', ''))
        )


class Payment(Operation):
    fields = (
        ('H', Header),
        ('B', PaymentBody),
    )

    def to_dict(self):
        o = self.as_dict()
        h = o['H'].as_dict()
        b = o['B'].as_dict()

        return dict(
            H=dict(
                type=h['Type'],
            ),
            B=dict(
                amount=b['Amount'],
                target=b['Target'],
            ),
        )

    @classmethod
    def from_dict(cls, d):
        assert d['H']['type'] == 'payment'

        return cls(
            H=Header(Type='payment'),
            B=PaymentBody(Target=d['B']['target'], Amount=d['B']['amount'])
        )


def create_account(target, amount, linked=''):
    assert type(amount) in (str,)

    return CreateAccount(
        H=Header(Type='create-account'),
        B=CreateAccountBody(Target=target, Amount=amount, Linked=linked)
    )


def payment(target, amount):
    assert type(amount) in (str,)

    return Payment(
        H=Header(Type='payment'),
        B=PaymentBody(Target=target, Amount=amount)
    )
