from os import path
from pathlib import Path

def projectroot() -> Path:
    return path.dirname(Path(__file__).parent)
