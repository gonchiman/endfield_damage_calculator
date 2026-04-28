import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "endfield.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
SEED_PATH = BASE_DIR / "sql" / "seed.sql"


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())

    with open(SEED_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()