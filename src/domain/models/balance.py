from tortoise import fields, Model

from src.domain.enums import Currency


class Balance(Model):
    class Meta:
        table = 'balances'
        unique_together = ('user', 'currency')

    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('models.User', related_name='balances')
    currency = fields.CharEnumField(Currency)
    value = fields.DecimalField(max_digits=8, decimal_places=8)

    def __str__(self):
        return f'{self.value:f} {self.currency}'

    def __repr__(self):
        return self.__str__()
