from dataclasses import dataclass

from src.constants.attack_attributes import AttackAttributes


@dataclass
class AttackHit:
    multiplier: int
    attribute: AttackAttributes