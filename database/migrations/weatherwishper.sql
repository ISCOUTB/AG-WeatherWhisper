CREATE SCHEMA `weatherwishper` ;
USE weatherwishper;
-- Tabla de usuarios
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    phone_number TEXT,
    age INT
);

-- Tabla de preferencias de clima de usuario
CREATE TABLE user_weather_preferences (
    id_preferences SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    temperature_unit TEXT,
    receive_alerts BOOLEAN,
    preferred_conditions TEXT
);

-- Tabla de ubicaciones de usuario
CREATE TABLE user_locations (
    id_location SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    latitude FLOAT8 NOT NULL,
    longitude FLOAT8 NOT NULL,
    address TEXT
);

-- Tabla de configuraciones de usuario
CREATE TABLE user_settings (
    id_settings SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    temperature_unit TEXT,
    language TEXT
);
