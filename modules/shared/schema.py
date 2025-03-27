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
        number VARCHAR(100) UNIQUE NOT NULL,
        folder VARCHAR(255),
        offence_id INTEGER NOT NULL REFERENCES offences(id) ON DELETE RESTRICT,
        operator_id INTEGER NOT NULL REFERENCES operators(id) ON DELETE RESTRICT,
        type VARCHAR(100) NOT NULL,
        origin VARCHAR(255),
        target_date DATE NOT NULL,
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT chk_type CHECK (type IN ('Person', 'Organization', 'Vehicle', 'Other'))
    );
    CREATE INDEX IF NOT EXISTS idx_targets_number ON targets(number);
    CREATE INDEX IF NOT EXISTS idx_targets_offence_id ON targets(offence_id);
    CREATE INDEX IF NOT EXISTS idx_targets_operator_id ON targets(operator_id);
    CREATE INDEX IF NOT EXISTS idx_targets_target_date ON targets(target_date);
"""

# List of table creation queries in order (respecting foreign key dependencies)
TABLES = [
    CREATE_USERS_TABLE,
    CREATE_USER_PROFILES_TABLE,
    CREATE_OFFENCES_TABLE,
    CREATE_OPERATORS_TABLE,
    CREATE_TARGETS_TABLE
]