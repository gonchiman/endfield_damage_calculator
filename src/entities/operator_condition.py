from dataclasses import dataclass


@dataclass
class OperatorCondition:
    operator_id: str
    operator_level: int