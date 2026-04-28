INSERT OR REPLACE INTO operators (
    operator_id,
    operator_name
) VALUES (
    'lifeng',
    'Lifeng'
);

INSERT OR REPLACE INTO operator_statuses (
    operator_id,
    level,
    strength,
    agility,
    intellect,
    will,
    base_atk
) VALUES 
    ('lifeng', 1, 14, 20, 13, 12, 30),
    ('lifeng', 20, 38, 44, 35, 35, 90),
    ('lifeng', 40, 62, 69, 58, 58, 153),
    ('lifeng', 60, 86, 94, 81, 82, 217),
    ('lifeng', 80, 111, 119, 104, 105, 280),
    ('lifeng', 90, 123, 132, 115, 117, 312);