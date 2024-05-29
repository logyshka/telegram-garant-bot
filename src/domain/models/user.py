from tortoise import fields, Model

from .balance import Balance
from .bill import Bill


class User(Model):
    class Meta:
        table = 'users'

    id = fields.BigIntField(primary_key=True)
    url = fields.CharField(max_length=150)
    locale_name = fields.CharField(max_length=5)
    balances: fields.BackwardFKRelation[Balance]
    bills: fields.BackwardFKRelation[Bill]
