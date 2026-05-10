CREATE TABLE IF NOT EXISTS operator_statuses (
    operator_id TEXT NOT NULL,
    level INTEGER NOT NULL,
    strength INTEGER NOT NULL,
    agility INTEGER NOT NULL,
    intellect INTEGER NOT NULL,
    will INTEGER NOT NULL,
    base_atk INTEGER NOT NULL,
    PRIMARY KEY (operator_id, level),
    FOREIGN KEY (operator_id) REFERENCES operator_master(operator_id)
);