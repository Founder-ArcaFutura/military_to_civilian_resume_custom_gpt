PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS mosids (
    mosid TEXT PRIMARY KEY,
    title TEXT
);

CREATE TABLE IF NOT EXISTS nocs (
    noc TEXT PRIMARY KEY,
    title TEXT
);

CREATE TABLE IF NOT EXISTS mosid_noc_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mosid TEXT NOT NULL,
    noc TEXT NOT NULL,
    UNIQUE (mosid, noc),
    FOREIGN KEY (mosid) REFERENCES mosids (mosid) ON DELETE CASCADE,
    FOREIGN KEY (noc) REFERENCES nocs (noc) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mosid_noc_titles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mapping_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    UNIQUE (mapping_id, title),
    FOREIGN KEY (mapping_id) REFERENCES mosid_noc_mappings (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mosid_noc_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mapping_id INTEGER NOT NULL,
    skill TEXT NOT NULL,
    UNIQUE (mapping_id, skill),
    FOREIGN KEY (mapping_id) REFERENCES mosid_noc_mappings (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mosid_noc_employment_contexts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mapping_id INTEGER NOT NULL,
    context TEXT NOT NULL,
    UNIQUE (mapping_id, context),
    FOREIGN KEY (mapping_id) REFERENCES mosid_noc_mappings (id) ON DELETE CASCADE
);
