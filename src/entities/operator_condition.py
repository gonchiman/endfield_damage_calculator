from dataclasses import dataclass


@dataclass
class OperatorCondition:
    operator_id: str
    level: int