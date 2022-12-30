from aiogram import types

from ..utils.paths import ROOT_PATH

ASSETS_PATH = ROOT_PATH / "assets"


class Asset:
    def __init__(self, filename: str):
        self.filepath = ASSETS_PATH / filename
        self.bytes = self.filepath.read_bytes()

    def to_input_file(self):
        return types.BufferedInputFile(self.bytes, self.filepath.name)
