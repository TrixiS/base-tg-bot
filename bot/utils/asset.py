import functools
from pathlib import Path

import aiofiles
from aiogram import types

from ..utils.paths import ROOT_PATH

ASSETS_PATH = ROOT_PATH / "assets"

AssetPath = Path | str


class Asset:
    def __init__(self, filename: str, bytes: bytes):
        self.filename = filename
        self.bytes = bytes

    @staticmethod
    def __get_asset_filepath(path: AssetPath):
        if isinstance(path, Path):
            return path

        return ASSETS_PATH / path

    @classmethod
    def from_file(cls, path: AssetPath):
        filepath = cls.__get_asset_filepath(path)

        with open(filepath, "rb") as f:
            return cls(filepath.name, f.read())

    @classmethod
    async def async_from_file(cls, path: AssetPath):
        filepath = cls.__get_asset_filepath(path)

        async with aiofiles.open(filepath, "rb") as f:
            return cls(filepath.name, await f.read())

    @functools.cached_property
    def input_file(self):
        return types.BufferedInputFile(self.bytes, self.filename)
