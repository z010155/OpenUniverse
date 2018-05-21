CREATE TABLE IF NOT EXISTS accounts (
    id                  BIGINT PRIMARY KEY,
    username            VARCHAR(66) NOT NULL,
    password            VARCHAR(512) NOT NULL,
    character           BIGINT
);

CREATE TABLE IF NOT EXISTS characters (
    id                  BIGINT PRIMARY KEY,
    name                VARCHAR(66) NOT NULL,
    account             BIGINT REFERENCES accounts(id) ON DELETE CASCADE,
    zone                SMALLINT NOT NULL DEFAULT 0,

-- stats
    max_armor           SMALLINT NOT NULL DEFAULT 0,
    armor               SMALLINT NOT NULL DEFAULT 0,
    max_health          SMALLINT NOT NULL DEFAULT 4,
    health              SMALLINT NOT NULL DEFAULT 4,
    imagination         SMALLINT NOT NULL DEFAULT 0,
    max_imagination     SMALLINT NOT NULL DEFAULT 6,
    immunity            BOOL NOT NULL DEFAULT FALSE,
    currency            INT NOT NULL DEFAULT 0,
    free_to_play        BOOL NOT NULL DEFAULT FALSE,
    gm_level            INT NOT NULL DEFAULT 0,
    lu_score            INT NOT NULL DEFAULT 0,
    playtime            BIGINT NOT NULL DEFAULT 0,
    emotes              INT[] NOT NULL DEFAULT '{}',
    worlds              INT[] NOT NULL DEFAULT '{}',
    level               INT NOT NULL DEFAULT 1,

-- appearance
    eyebrow_style       INT NOT NULL,
    eye_styte           INT NOT NULL,
    hair_color          INT NOT NULL,
    hair_style          INT NOT NULL,
    pants_color         INT NOT NULL,
    mouth_style         INT NOT NULL,
    shirt_color         INT NOT NULL,
    shirt_style         INT NOT NULL,

-- unknown
    lh                  VARCHAR NOT NULL,
    rh                  VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS missions (
    id                  SMALLINT NOT NULL,
    state               SMALLINT NOT NULL DEFAULT 2,
    progress            INT NOT NULL DEFAULT 0,
    times_completed     INT NOT NULL DEFAULT 0,
    last_completion     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    character           BIGINT REFERENCES characters(id) ON DELETE CASCADE
);
