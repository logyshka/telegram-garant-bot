from tortoise import Model, fields


class Ban(Model):
    class Meta:
        table = 'ban'

    user_id = fields.IntField(primary_key=True)
    reason = fields.CharField(max_length=100, null=True)
    till = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
