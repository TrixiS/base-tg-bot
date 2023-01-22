import functools
from pathlib import Path

import aiofiles
from aiogram import types

from ..utils.paths import ROOT_PATH

ASSETS_PATH = ROOT_PATH / "assets"

AssetPath = Path | str


class Asset:
    def __init__(self, path: AssetPath, bytes: bytes):
        self.path = self.__get_asset_filepath(path)
        self.bytes = bytes

    @staticmethod
    def __get_asset_filepath(path: AssetPath):
        if isinstance(path, Path):
            return path

        return ASSETS_PATH / path

    @classmethod
    def from_file(cls, path: AssetPath):
        with open(path, "rb") as f:
            return cls(path, f.read())

    @classmethod
    async def async_from_file(cls, path: AssetPath):
        async with aiofiles.open(path, "rb") as f:
            return cls(path, await f.read())

    @functools.cached_property
    def input_file(self):
        return types.BufferedInputFile(self.bytes, self.path.name)
