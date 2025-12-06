import html

from tortoise import fields
from tortoise.models import Model


class BotUser(Model):
    id = fields.BigIntField(pk=True, unique=True, generated=False)  # telegram user id
    username = fields.TextField(null=True)
    first_name = fields.TextField()
    last_name = fields.TextField(null=True)
    joined_at = fields.DatetimeField(auto_now_add=True)
    left_at = fields.DatetimeField(null=True)

    @property
    def full_name(self) -> str:
        if self.last_name:
            return html.escape(f"{self.first_name} {self.last_name}")

        return html.escape(self.first_name)

    @property
    def mention(self):
        if self.username:
            return f"@{self.username}"

        return f'<a href="tg://user?id={self.id}">{self.full_name}</a>'
