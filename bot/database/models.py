from tortoise import fields
from tortoise.models import Model


class BotUser(Model):
    id = fields.IntField(pk=True, unique=True)  # telegram user id
    username = fields.TextField(null=True)
    full_name = fields.TextField()

    @property
    def mention(self):
        if self.username:
            return f"@{self.username}"

        return f'<a href="tg://user?id={self.id}">{self.full_name}</a>'

    @property
    def url(self):
        if self.username:
            return f"https://t.me/{self.username}"

        return f"tg://user?id={self.id}"
