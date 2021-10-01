import json

from pathlib import Path
from pydantic import BaseModel
from bot import models, root_path

CONFIG_FILENAMES = ("config.json", "config_dev.json")


def _update_model_json_file(model_cls: BaseModel, filepath: Path):
    model_object = model_cls.parse_file(filepath)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(model_object.dict(), f, indent=2, ensure_ascii=False)


def update_config_json_file(config_path: Path):
    _update_model_json_file(models.ConfigModel, config_path)


def update_phrases_json_file(phrases_path: Path):
    _update_model_json_file(models.PhrasesModel, phrases_path)


def main():
    for config_filename in CONFIG_FILENAMES:
        path = root_path / config_filename

        if not path.exists():
            continue

        update_config_json_file(path)

    update_phrases_json_file(root_path / "phrases.json")


if __name__ == "__main__":
    main()
