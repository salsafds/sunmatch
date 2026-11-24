import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "sunmatch.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_alternatif():
    with get_connection() as con:
        return pd.read_sql("SELECT * FROM alternatif", con)