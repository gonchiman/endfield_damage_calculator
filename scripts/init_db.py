import csv
import sqlite3
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.constants.database_columns import (
    OperatorStatusesColumns, 
    OperatorsColumns,
)


SQL_DIR = BASE_DIR / "sql"

DB_PATH = BASE_DIR / "data" / "endfield.db"

SCHEMA_PATH = SQL_DIR / "schema.sql"
INSERT_OPERATORS_SQL_PATH = SQL_DIR / "insert_operators.sql"
INSERT_OPERATOR_STATUSES_SQL_PATH = SQL_DIR / "insert_operator_statuses.sql"

OPERATORS_CSV_PATH = BASE_DIR / "data" / "csv" / "operators.csv"
OPERATOR_STATUSES_CSV_PATH = BASE_DIR / "data" / "csv" / "operator_statuses.csv"


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, encoding="utf-8", newline="") as f:
        conn.executescript(f.read())

    insert_operators(conn)
    insert_operator_statuses(conn)

    conn.commit()
    conn.close()


def insert_operators(conn):
    with open(OPERATORS_CSV_PATH, encoding="utf-8", newline="") as f_csv, \
        open(INSERT_OPERATORS_SQL_PATH, encoding="utf-8") as f_sql:
        reader = csv.DictReader(f_csv)
        insert_sql = f_sql.read()

        for row in reader:
            conn.execute(
                insert_sql, 
                (
                    row[OperatorsColumns.OPERATOR_ID],
                    row[OperatorsColumns.OPERATOR_NAME],
                 ),
            )


def insert_operator_statuses(conn):
    with open(OPERATOR_STATUSES_CSV_PATH, encoding="utf-8", newline="") as f_csv, \
        open(INSERT_OPERATOR_STATUSES_SQL_PATH, encoding="utf-8") as f_sql:
        reader = csv.DictReader(f_csv)
        insert_sql = f_sql.read()

        for row in reader:
            conn.execute(
                insert_sql,
                (
                    row[OperatorStatusesColumns.OPERATOR_ID],
                    int(row[OperatorStatusesColumns.LEVEL]),
                    int(row[OperatorStatusesColumns.STRENGTH]),
                    int(row[OperatorStatusesColumns.AGILITY]),
                    int(row[OperatorStatusesColumns.INTELLECT]),
                    int(row[OperatorStatusesColumns.WILL]),
                    int(row[OperatorStatusesColumns.BASE_ATK]),
                ),
            )


if __name__ == "__main__":
    init_db()