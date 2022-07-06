from aiogram import Dispatcher

from .bot_user import BotUserMiddleware


def setup(dispatcher: Dispatcher):
    bot_user_middleware = BotUserMiddleware()
    dispatcher.message.middleware.register(bot_user_middleware)
    dispatcher.callback_query.middleware.register(bot_user_middleware)
