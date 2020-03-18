from os import path
from pathlib import Path

def projectroot() -> str:
    return path.dirname(Path(__file__).parent)
