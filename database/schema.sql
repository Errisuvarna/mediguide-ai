-- MediGuide AI Database Schema (SQLite-compatible; portable to PostgreSQL)
-- Run automatically via SQLAlchemy models on first app startup.
-- This file is the human-readable reference copy of that same schema.

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'staff',
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_users_email ON users(email);

CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL UNIQUE,
    description TEXT,
    floor_number INTEGER,
    building_name VARCHAR(120),
    contact_number VARCHAR(30),
    office_hours VARCHAR(120),
    avg_waiting_time_minutes INTEGER DEFAULT 15,
    keywords TEXT
);
CREATE INDEX idx_departments_name ON departments(name);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(120) NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    designation VARCHAR(120),
    qualification VARCHAR(160),
    consultation_fee FLOAT DEFAULT 0,
    room_number VARCHAR(20),
    available_days VARCHAR(80),
    available_time VARCHAR(60),
    experience_years INTEGER DEFAULT 0
);

CREATE TABLE doctor_specializations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    specialization VARCHAR(120) NOT NULL
);

CREATE TABLE buildings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE floors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_id INTEGER NOT NULL REFERENCES buildings(id),
    floor_number INTEGER NOT NULL,
    label VARCHAR(80)
);

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    floor_id INTEGER NOT NULL REFERENCES floors(id),
    room_number VARCHAR(20) NOT NULL,
    room_type VARCHAR(60),
    department_name VARCHAR(120)
);

CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    description TEXT,
    fee FLOAT DEFAULT 0,
    location VARCHAR(120)
);

CREATE TABLE procedures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    estimated_cost FLOAT DEFAULT 0,
    prep_instructions TEXT
);

CREATE TABLE required_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_name VARCHAR(120) NOT NULL,
    document_name VARCHAR(150) NOT NULL,
    is_mandatory VARCHAR(10) DEFAULT 'yes',
    notes TEXT
);

CREATE TABLE hospital_map_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(60),
    building_name VARCHAR(120),
    floor_number INTEGER,
    x_coordinate FLOAT NOT NULL,
    y_coordinate FLOAT NOT NULL,
    description TEXT
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name VARCHAR(120) NOT NULL,
    patient_contact VARCHAR(30),
    doctor_id INTEGER REFERENCES doctors(id),
    department_id INTEGER REFERENCES departments(id),
    scheduled_time DATETIME,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(80),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    keywords VARCHAR(255)
);

CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120),
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analytics_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type VARCHAR(40) NOT NULL,
    department VARCHAR(120),
    language VARCHAR(10) DEFAULT 'en',
    is_voice INTEGER DEFAULT 0,
    is_emergency INTEGER DEFAULT 0,
    response_time_ms FLOAT DEFAULT 0,
    was_answered INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_analytics_created_at ON analytics_events(created_at);

CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(64) NOT NULL,
    role VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'en',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_chat_history_session ON chat_history(session_id);

CREATE TABLE knowledge_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file VARCHAR(150) NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL
);
