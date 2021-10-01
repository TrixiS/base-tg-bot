from pathlib import Path

__title__ = "bot"
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .models import ConfigModel, PhrasesModel
from . import *

root_path = Path(__file__).parent.parent
config_path = root_path / "config.json"
config_dev_path = root_path / "config_dev.json"

config = ConfigModel.parse_file(
    config_dev_path if config_dev_path.exists() else config_path
)

phrases = PhrasesModel.parse_file(root_path / "phrases.json")
