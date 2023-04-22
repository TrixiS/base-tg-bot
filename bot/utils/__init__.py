from prisma.models import BotUser


def get_bot_user_mention(bot_user: BotUser):
    if bot_user.username:
        return f"@{bot_user.username}"

    return f'<a href="tg://user?id={bot_user.id}">{bot_user.full_name}</a>'


def get_bot_user_url(bot_user: BotUser):
    if bot_user.username:
        return f"https://t.me/{bot_user.username}"

    return f"tg://user?id={bot_user.id}"
