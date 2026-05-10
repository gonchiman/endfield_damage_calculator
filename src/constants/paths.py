from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "endfield.db"

SQL_DIR = BASE_DIR / "sql"
OPERATOR_MASTER_SQL_PATH = SQL_DIR / "operator_master.sql"
OPERATOR_STATUSES_SQL_PATH = SQL_DIR / "operator_statuses.sql"
OPERATOR_ATTACK_HITS_SQL_PATH = SQL_DIR / "operator_attack_hits.sql"

CSV_DIR = DATA_DIR / "csv"
OPERATOR_MASTER_CSV_PATH = CSV_DIR / "operator_master.csv"
OPERATOR_STATUSES_CSV_PATH = CSV_DIR / "operator_statuses.csv"
OPERATOR_ATTACK_HITS_CSV_PATH = CSV_DIR / "operator_attack_hits.csv"
