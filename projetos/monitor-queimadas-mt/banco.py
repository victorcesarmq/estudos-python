import pandas as pd
import sqlite3
from pathlib import Path


class Banco:
    def __init__(self):
        self.path = Path("dados")
