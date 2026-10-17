import sqlite3
from pathlib import Path

import pytest


@pytest.fixture
def db_connection():
    db_path = Path(__file__).parent.parent / "data" / "revelio_practice.db"
    connection = sqlite3.connect(db_path)

    yield connection

    connection.close()