CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) DEFAULT 'parent'
);

CREATE TABLE IF NOT EXISTS campers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    parent_id INTEGER,
    emergency_contact_name VARCHAR(255),
    emergency_phone VARCHAR(20),
    medical_notes TEXT,
    is_active BOOLEAN DEFAULT true
);

INSERT INTO users (email, password_hash) VALUES ('admin@camp.com', 'admin123') ON CONFLICT DO NOTHING;
