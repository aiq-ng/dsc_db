# modules/shared/schema.py

CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_USER_PROFILES_TABLE = """
    CREATE TABLE IF NOT EXISTS user_profiles (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        full_name VARCHAR(255),
        bio TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_OFFENCES_TABLE = """
    CREATE TABLE IF NOT EXISTS offences (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_offences_name ON offences(name);
"""

CREATE_REQUEST_TYPES_TABLE = """
    CREATE TABLE IF NOT EXISTS request_types (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_OPERATORS_TABLE = """
    CREATE TABLE IF NOT EXISTS operators (
        id SERIAL PRIMARY KEY,
        operator_name VARCHAR(255) NOT NULL,
        operator_code VARCHAR(50) UNIQUE NOT NULL,
        contact_info JSONB DEFAULT '{}',
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_operators_operator_code ON operators(operator_code);
"""

CREATE_TARGETS_TABLE = """
    CREATE TABLE IF NOT EXISTS targets (
        id SERIAL PRIMARY KEY,
        target_name VARCHAR(255) NOT NULL,
        file_number VARCHAR(100) UNIQUE NOT NULL,
        target_number VARCHAR(100),
        folder VARCHAR(255),
        offence_id INTEGER NOT NULL REFERENCES offences(id) ON DELETE RESTRICT,
        operator_id INTEGER NOT NULL REFERENCES operators(id) ON DELETE RESTRICT,
        type VARCHAR(100),
        type_id INTEGER,
        origin VARCHAR(255),
        target_date DATE NOT NULL,
        metadata JSONB DEFAULT '{}',
        flagged BOOLEAN DEFAULT FALSE,
        threat_level VARCHAR(50) DEFAULT 'Low' CHECK (threat_level IN ('High', 'Medium', 'Low')),  -- New column
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_targets_file_number ON targets(file_number);
    CREATE INDEX IF NOT EXISTS idx_targets_target_number ON targets(target_number);
    CREATE INDEX IF NOT EXISTS idx_targets_offence_id ON targets(offence_id);
    CREATE INDEX IF NOT EXISTS idx_targets_operator_id ON targets(operator_id);
    CREATE INDEX IF NOT EXISTS idx_targets_target_date ON targets(target_date);
    CREATE INDEX IF NOT EXISTS idx_targets_flagged ON targets(flagged);
    CREATE INDEX IF NOT EXISTS idx_targets_threat_level ON targets(threat_level);  -- New index
"""


CREATE_SUGGESTIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS suggestions (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_suggestions_user_id ON suggestions(user_id);
"""

TABLES = [
    CREATE_USERS_TABLE,
    CREATE_USER_PROFILES_TABLE,
    CREATE_OFFENCES_TABLE,
    CREATE_REQUEST_TYPES_TABLE,
    CREATE_OPERATORS_TABLE,
    CREATE_TARGETS_TABLE,
    CREATE_SUGGESTIONS_TABLE,  # Add this
]
