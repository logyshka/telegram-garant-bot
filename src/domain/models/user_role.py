from tortoise import fields, Model

from src.domain.enums import Role


class UserRole(Model):
    class Meta:
        table = 'user-roles'

    user_id = fields.IntField(primary_key=True)
    role = fields.CharEnumField(Role)
    constant = fields.BooleanField()
