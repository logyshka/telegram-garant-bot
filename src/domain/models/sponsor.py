from tortoise import Model, fields


class Sponsor(Model):
    class Meta:
        table = 'sponsors'

    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=150)
    invite_link = fields.CharField(max_length=150)
    creates_join_request = fields.BooleanField()
    expire_date = fields.DatetimeField(null=True)
