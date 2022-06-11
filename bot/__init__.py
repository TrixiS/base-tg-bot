from pathlib import Path

__title__ = "bot"
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from . import *

ENCODING = "utf-8-sig"

root_path = Path(__file__).parent.parent
routers_path = root_path / "bot/routers"
