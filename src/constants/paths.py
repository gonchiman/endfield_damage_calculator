from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "endfield.db"

SQL_DIR = BASE_DIR / "sql"
SCHEMA_PATH = SQL_DIR / "schema.sql"
INSERT_OPERATOR_MASTER_SQL_PATH = SQL_DIR / "insert_operator_master.sql"
INSERT_OPERATOR_STATUSES_SQL_PATH = SQL_DIR / "insert_operator_statuses.sql"

CSV_DIR = DATA_DIR / "csv"
OPERATOR_MASTER_CSV_PATH = CSV_DIR / "operator_master.csv"
OPERATOR_STATUSES_CSV_PATH = CSV_DIR / "operator_statuses.csv"