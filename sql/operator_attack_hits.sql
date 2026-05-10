CREATE TABLE IF NOT EXISTS operator_attack_hits (
    operator_id TEXT NOT NULL,
    attack_type TEXT NOT NULL,
    rank INTEGER NOT NULL,
    attack_step INTEGER NOT NULL,
    multiplier INTEGER NOT NULL,
    damage_type TEXT NOT NULL,

    PRIMARY KEY (operator_id, attack_type, rank, attack_step),
    FOREIGN KEY (operator_id) REFERENCES operator_master(operator_id)
);