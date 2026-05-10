CREATE TABLE IF NOT EXISTS operator_master (
    operator_id TEXT PRIMARY KEY,
    operator_name TEXT NOT NULL,
    main_stat TEXT NOT NULL,
    sub_stat TEXT NOT NULL
);