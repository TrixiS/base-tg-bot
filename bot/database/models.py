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
        return f"{self.first_name} {self.last_name}"

    @property
    def tg_url(self) -> str:
        return f"tg://user?id={self.id}"

    @property
    def url(self):
        if self.username:
            return f"https://t.me/{self.username}"

        return self.tg_url

    @property
    def mention(self):
        if self.username:
            return f"@{self.username}"

        return f'<a href="{self.tg_url}">{self.full_name}</a>'


class BotChat(Model):
    id = fields.BigIntField(
        pk=True, unique=True, generated=False
    )  # telegram chat id signed
    title = fields.TextField()
    username = fields.TextField(null=True)
    type = fields.TextField()
