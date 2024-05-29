from tortoise import fields, Model

from src.domain.enums import Currency


class Bill(Model):
    class Meta:
        table = 'bills'

    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('models.User', related_name='bills')
    currency = fields.CharEnumField(Currency)
    amount = fields.DecimalField(max_digits=8, decimal_places=8)
    payment = fields.CharField(max_length=50)
    payment_display_name = fields.CharField(max_length=50)
    is_paid = fields.BooleanField(default=False)
    pay_url = fields.CharField(max_length=150)
    check_info = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    expires_at = fields.DatetimeField(null=True)

    @property
    def amount_str(self) -> str:
        return f'{self.amount:f} {self.currency}'

    def __str__(self):
        return f'{self.amount:f} {self.currency} | {self.payment}'

    def __repr__(self):
        return self.__str__()
