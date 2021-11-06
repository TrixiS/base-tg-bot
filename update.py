from pathlib import Path

from pydantic import BaseModel

from bot import root_path
from bot.config import BotConfig
from bot.phrases import BotPhrases


def update_json_file_from_model(path: Path, model_cls: BaseModel):
    if not path.exists():
        return

    model_object = model_cls.parse_file(path)

    with open(path, "w", encoding="utf-8") as f:
        json_string = model_object.json(indent=2, ensure_ascii=False)
        f.write(json_string)


def update_config_files():
    for config_filename in BotConfig.__config_filenames__:
        update_json_file_from_model(root_path / config_filename, BotConfig)


def update_phrase_files():
    for phrases_path in (root_path / "phrases").glob("*.json"):
        update_json_file_from_model(phrases_path, BotPhrases)


def main():
    update_config_files()
    update_phrase_files()


if __name__ == "__main__":
    main()
