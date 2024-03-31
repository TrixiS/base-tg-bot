from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
ROUTERS_PATH = ROOT_PATH / f"{__name__.split('.')[0]}/routers"
