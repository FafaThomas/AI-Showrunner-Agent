-- ==========================================
-- FACT_SLOT_PERFORMANCE
-- Grain:
-- One row = One program airing in one slot
-- on one broadcast date.
-- ==========================================

CREATE TABLE slot (
    slot_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    start_time TIME NOT NULL,
    end_time TIME NOT NULL,

    duration_minutes INTEGER NOT NULL,

    slot_name VARCHAR(50),
    daypart VARCHAR(20),

    is_prime_time BOOLEAN NOT NULL DEFAULT FALSE,

    UNIQUE (start_time, end_time)
);

CREATE TABLE program (
    program_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    title VARCHAR(255) NOT NULL UNIQUE,

    program_type VARCHAR(50) NOT NULL,
    -- Series
    -- Cinema
    -- News
    -- Sports
    -- Special

    genre VARCHAR(100),

    duration_minutes INTEGER NOT NULL,

    content_rating VARCHAR(20),

    target_demographic VARCHAR(100)
);

CREATE TABLE slot_program (
    slot_program_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    slot_key INTEGER NOT NULL REFERENCES slot(slot_key),

    broadcast_date DATE NOT NULL,

    program_key INTEGER NOT NULL REFERENCES program(program_key),

    slot_order INTEGER DEFAULT 1,

    UNIQUE (
        slot_key,
        broadcast_date
    )
);

CREATE TABLE commercial (
    commercial_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    brand_name VARCHAR(255) NOT NULL,

    campaign_name VARCHAR(255),

    duration_seconds INTEGER NOT NULL,

    target_demographic VARCHAR(100),

    campaign_start DATE,

    campaign_end DATE

    UNIQUE (brand_name, campaign_name)
    
);


CREATE TABLE slot_commercial (
    slot_commercial_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    slot_key INTEGER NOT NULL REFERENCES slot(slot_key),

    broadcast_date DATE NOT NULL,

    commercial_key INTEGER NOT NULL REFERENCES commercial(commercial_key),

    sequence_order INTEGER NOT NULL
);

CREATE TABLE slot_viewership (
    slot_viewership_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    slot_key INTEGER NOT NULL REFERENCES slot(slot_key),

    broadcast_date DATE NOT NULL,

    viewer_count BIGINT NOT NULL,

    avg_watch_minutes NUMERIC(5,2),

    retention_rate NUMERIC(5,4),

    dropoff_rate NUMERIC(5,4),

    ad_revenue NUMERIC(15,2)
);


