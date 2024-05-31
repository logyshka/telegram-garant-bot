from tortoise import fields, Model

from .balance import Balance
from .bill import Bill
from ..enums import LocaleName


class User(Model):
    class Meta:
        table = 'users'

    id = fields.BigIntField(primary_key=True)
    locale_name = fields.CharEnumField(LocaleName, null=True)
    balances: fields.BackwardFKRelation[Balance]
    bills: fields.BackwardFKRelation[Bill]
