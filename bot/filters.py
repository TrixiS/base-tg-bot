from .config import config


def is_admin(user_id: int):
    return config.admin_user_id == user_id


def admin_filter(_, is_admin: bool):
    return is_admin
