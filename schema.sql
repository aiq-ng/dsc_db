
CREATE TABLE IF NOT EXISTS user_profiles (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        full_name VARCHAR(255),
        bio TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );


CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );


CREATE TABLE IF NOT EXISTS offences (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX idx_offences_name ON offences(name);

CREATE TABLE IF NOT EXISTS request_types (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX idx_request_types_name ON request_types(name);

CREATE TABLE IF NOT EXISTS operators (
        id SERIAL PRIMARY KEY,
        operator_name VARCHAR(255) NOT NULL,
        operator_code VARCHAR(50) UNIQUE NOT NULL,
        contact_info JSONB DEFAULT '{}',
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX idx_operators_operator_code ON operators(operator_code);

CREATE TABLE IF NOT EXISTS targets (
        id SERIAL PRIMARY KEY,
        target_name VARCHAR(255) NOT NULL,
        file_number VARCHAR(100) UNIQUE NOT NULL, -- Renamed from 'number'
        target_number VARCHAR(100), -- Added target_number
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
    CREATE INDEX IF NOT EXISTS idx_targets_file_number ON targets(file_number); --renamed index
    CREATE INDEX IF NOT EXISTS idx_targets_target_number ON targets(target_number); --added index
    CREATE INDEX IF NOT EXISTS idx_targets_offence_id ON targets(offence_id);
    CREATE INDEX IF NOT EXISTS idx_targets_operator_id ON targets(operator_id);
    CREATE INDEX IF NOT EXISTS idx_targets_target_date ON targets(target_date);
