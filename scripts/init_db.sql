CREATE TABLE vehicles (
    plate_id SERIAL PRIMARY KEY,
    plate_number VARCHAR(15) NOT NULL UNIQUE,
    region VARCHAR(3) NOT NULL CHECK (region ~ '^[А-Я]{0-9]{1,3}$'),
    vehicle_type VARCHAR(20) CHECK (vehicle_type IN ('легковой', 'грузовой', 'спецтранспорт')),
    is_commercial BOOLEAN DEFAULT FALSE,
    registration_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP WITH TIME ZONE
);

CREATE TABLE recognition_events (
    event_id BIGSERIAL PRIMARY KEY,
    plate_id INTEGER REFERENCES vehicles(plate_id),
    camera_id INTEGER NOT NULL,
    recognition_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    confidence NUMERIC(3,2) CHECK (confidence BETWEEN 0.00 AND 1.00),
    direction VARCHAR(10) CHECK (direction IN ('въезд', 'выезд')),
    image_path VARCHAR(255),
    coordinates GEOMETRY(POINT, 4326), -- PostGIS для геолокации
    is_verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE blacklist (
    record_id SERIAL PRIMARY KEY,
    plate_id INTEGER REFERENCES vehicles(plate_id),
    reason TEXT NOT NULL,
    added_by INTEGER NOT NULL, -- ID сотрудника
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(30) NOT NULL,
    department VARCHAR(30),
    access_level INTEGER CHECK (access_level BETWEEN 1 AND 3),
    login VARCHAR(30) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE
);

CREATE TABLE camera_settings (
    camera_id SERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    ip_address INET NOT NULL,
    model VARCHAR(50),
    resolution VARCHAR(10) DEFAULT '1920x1080',
    fps INTEGER DEFAULT 25,
    is_active BOOLEAN DEFAULT TRUE,
    last_maintenance DATE
);

CREATE TABLE parking_slots (
    slot_id SERIAL PRIMARY KEY,
    zone VARCHAR(2) NOT NULL, -- A, B, C...
    number INTEGER NOT NULL,
    status VARCHAR(15) DEFAULT 'free' CHECK (status IN ('free', 'occupied', 'reserved')),
    current_plate_id INTEGER REFERENCES vehicles(plate_id),
    occupied_since TIMESTAMP WITH TIME ZONE
);

CREATE TABLE access_rules (
    rule_id SERIAL PRIMARY KEY,
    vehicle_type VARCHAR(20),
    time_from TIME,
    time_to TIME,
    days_of_week VARCHAR(13) CHECK (days_of_week ~ '^[0-7,]{1,13}$'), -- 1,2,3,4,5
    is_holiday_exception BOOLEAN DEFAULT FALSE,
    description TEXT
);

CREATE INDEX idx_vehicles_plate ON vehicles (plate_number, region);
CREATE INDEX idx_events_plate ON recognition_events (plate_id);
CREATE INDEX idx_events_time ON recognition_events (recognition_time);
CREATE INDEX idx_blacklist_active ON blacklist (is_active, expires_at);
CREATE INDEX idx_employees_dept ON employees (department);
CREATE INDEX idx_cameras_location ON camera_settings (location);
CREATE UNIQUE INDEX idx_slots_unique ON parking_slots (zone, number);