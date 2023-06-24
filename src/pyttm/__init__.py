# __init__.py

from pathlib import Path
__version__ = open(Path(__file__).parent.joinpath('version.txt')).read().strip()


