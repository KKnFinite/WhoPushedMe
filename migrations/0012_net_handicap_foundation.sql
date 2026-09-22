ALTER TABLE golfers
    ADD COLUMN handicap_index numeric(4,1)
        CHECK (
            handicap_index IS NULL
            OR handicap_index BETWEEN -10.0 AND 54.0
        );

ALTER TABLE rounds
    ADD COLUMN net_scoring_enabled boolean NOT NULL DEFAULT false;

ALTER TABLE round_participants
    ADD COLUMN handicap_index numeric(4,1)
        CHECK (
            handicap_index IS NULL
            OR handicap_index BETWEEN -10.0 AND 54.0
        ),
    ADD COLUMN round_handicap smallint
        CHECK (
            round_handicap IS NULL
            OR round_handicap BETWEEN -20 AND 80
        ),
    ADD COLUMN handicap_source varchar(24)
        CHECK (
            handicap_source IS NULL
            OR handicap_source IN ('course', 'manual')
        );

CREATE TABLE cached_course_tee_ratings (
    course_id uuid NOT NULL REFERENCES cached_courses(id) ON DELETE CASCADE,
    tee_name text NOT NULL CHECK (length(btrim(tee_name)) > 0),
    gender varchar(16) NOT NULL DEFAULT 'unspecified',
    course_rating numeric(4,1)
        CHECK (
            course_rating IS NULL
            OR course_rating BETWEEN 40.0 AND 100.0
        ),
    slope_rating smallint
        CHECK (
            slope_rating IS NULL
            OR slope_rating BETWEEN 55 AND 155
        ),
    PRIMARY KEY (course_id, tee_name, gender)
);

CREATE INDEX cached_course_tee_ratings_lookup_idx
    ON cached_course_tee_ratings(course_id, lower(tee_name));
