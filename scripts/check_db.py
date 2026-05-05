import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.repositories.operator_status_repository import OperatorStatusRepository
from src.repositories.operator_master_repository import OperatorMasterRepository # noqa: E402


operators = OperatorMasterRepository.find_all()

print("operator master")
for operator in operators:
    print(operator)

print()
print("operator statuses")
statuses = OperatorStatusRepository.find_all()

for status in statuses:
    print(status)