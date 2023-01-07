from tortoise import fields
from tortoise.models import Model


class BotUser(Model):
    id = fields.IntField(pk=True, unique=True)  # telegram user id
    username = fields.TextField(null=True)
    full_name = fields.TextField()

    @property
    def link(self):
        if self.username:
            return f"@{self.username}"

        return f'<a href="tg://user?id={self.id}">{self.full_name}</a>'
