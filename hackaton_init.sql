CREATE TABLE user_table (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    version integer NOT NULL DEFAULT 1,
    login text NOT NULL CHECK (length(login) >= 6 AND length(login) <= 20),
    password_hash bytea NOT NULL CHECK (octet_length(password_hash) = 40),
    created_at timestamptz DEFAULT current_timestamp,
    updated_at timestamptz DEFAULT current_timestamp,
    
    CONSTRAINT user_login_unique UNIQUE (login)
);

CREATE TABLE observation_groups (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100),
    description TEXT,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'processing', 'completed', 'error')),
    created_at timestamptz DEFAULT current_timestamp,
    updated_at timestamptz DEFAULT current_timestamp
);


-- Таблица наблюдений
CREATE TABLE observations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES user_table(id) ON DELETE CASCADE,
    group_id uuid NOT NULL REFERENCES observation_groups(id) ON DELETE CASCADE,
    observation_time timestamptz NOT NULL,
    right_ascension DOUBLE PRECISION NOT NULL,  -- прямое восхождение в градусах
    declination DOUBLE PRECISION NOT NULL,      -- склонение в градусах
    observer_name VARCHAR(100),                 -- кто наблюдал
    observation_notes TEXT,                     -- заметки к наблюдению
    image_url VARCHAR(500),                     -- URL фотографии наблюдения
    created_at timestamptz DEFAULT current_timestamp,
    
    CONSTRAINT valid_ra CHECK (right_ascension >= 0 AND right_ascension < 360),
    CONSTRAINT valid_dec CHECK (declination >= -90 AND declination <= 90)
);

-- Таблица параметров орбиты
CREATE TABLE orbital_parameters (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id uuid NOT NULL REFERENCES observation_groups(id) ON DELETE CASCADE,
    semi_major_axis DOUBLE PRECISION NOT NULL,      -- большая полуось в а.е.
    eccentricity DOUBLE PRECISION NOT NULL,         -- эксцентриситет
    inclination DOUBLE PRECISION NOT NULL,          -- наклонение в градусах
    longitude_ascending_node DOUBLE PRECISION NOT NULL, -- долгота восходящего узла в градусах
    argument_perihelion DOUBLE PRECISION NOT NULL,  -- аргумент перицентра в градусах
    time_perihelion timestamptz NOT NULL,           -- время прохождения перигелия
    calculation_date timestamptz DEFAULT current_timestamp,
    used_observations_count INTEGER NOT NULL,       -- сколько наблюдений использовалось
    
    CONSTRAINT positive_semi_major_axis CHECK (semi_major_axis > 0),
    CONSTRAINT valid_eccentricity CHECK (eccentricity >= 0),
    CONSTRAINT valid_inclination CHECK (inclination >= 0 AND inclination <= 180),
    CONSTRAINT valid_angles CHECK (
        longitude_ascending_node >= 0 AND longitude_ascending_node < 360 AND
        argument_perihelion >= 0 AND argument_perihelion < 360
    )
);

-- Таблица результатов сближения
CREATE TABLE close_approaches (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id uuid NOT NULL REFERENCES observation_groups(id) ON DELETE CASCADE,
    orbital_parameters_id uuid NOT NULL REFERENCES orbital_parameters(id) ON DELETE CASCADE,
    approach_time timestamptz NOT NULL,    -- время сближения
    distance_au DOUBLE PRECISION NOT NULL,              -- дистанция в а.е.
    distance_km DOUBLE PRECISION NOT NULL,              -- дистанция в км
    calculation_date timestamptz DEFAULT current_timestamp,
    
    CONSTRAINT positive_distance CHECK (distance_au > 0 AND distance_km > 0)
);


-- Функция для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Триггеры для автоматического обновления updated_at
CREATE TRIGGER update_user_table_updated_at BEFORE UPDATE ON user_table
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_observation_groups_updated_at BEFORE UPDATE ON observation_groups
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();