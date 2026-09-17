CREATE TABLE golfers (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name varchar(40) NOT NULL CHECK (length(btrim(display_name)) BETWEEN 1 AND 40),
    recovery_key char(7) NOT NULL UNIQUE
        CHECK (recovery_key ~ '^[A-HJ-KM-NP-Z2-9]{3}-[A-HJ-KM-NP-Z2-9]{3}$'),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE cached_courses (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    provider varchar(32) NOT NULL DEFAULT 'opengolfapi',
    external_course_id text NOT NULL,
    name text NOT NULL CHECK (length(btrim(name)) > 0),
    cached_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (provider, external_course_id)
);

CREATE TABLE cached_course_holes (
    course_id uuid NOT NULL REFERENCES cached_courses(id) ON DELETE CASCADE,
    hole_number smallint NOT NULL CHECK (hole_number BETWEEN 1 AND 18),
    par smallint CHECK (par BETWEEN 2 AND 7),
    stroke_index smallint CHECK (stroke_index BETWEEN 1 AND 18),
    PRIMARY KEY (course_id, hole_number)
);

CREATE TABLE cached_course_hole_tees (
    course_id uuid NOT NULL,
    hole_number smallint NOT NULL,
    tee_name text NOT NULL CHECK (length(btrim(tee_name)) > 0),
    yardage smallint CHECK (yardage > 0),
    PRIMARY KEY (course_id, hole_number, tee_name),
    FOREIGN KEY (course_id, hole_number)
        REFERENCES cached_course_holes(course_id, hole_number) ON DELETE CASCADE
);

CREATE TABLE rounds (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    mode varchar(16) NOT NULL CHECK (mode IN ('individual', 'scramble')),
    hole_count smallint NOT NULL CHECK (hole_count IN (9, 18)),
    active_code char(4) NOT NULL CHECK (active_code ~ '^[0-9]{4}$'),
    current_hole smallint NOT NULL DEFAULT 1,
    status varchar(16) NOT NULL DEFAULT 'active'
        CHECK (status IN ('setup', 'active', 'completed', 'abandoned')),
    course_id uuid REFERENCES cached_courses(id) ON DELETE SET NULL,
    free_play_name text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (current_hole BETWEEN 1 AND hole_count),
    CHECK (free_play_name IS NULL OR length(btrim(free_play_name)) > 0)
);

CREATE UNIQUE INDEX rounds_live_code_unique
    ON rounds(active_code)
    WHERE status IN ('setup', 'active');

CREATE TABLE round_participants (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    round_id uuid NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
    golfer_id uuid NOT NULL REFERENCES golfers(id) ON DELETE RESTRICT,
    role varchar(16) NOT NULL CHECK (role IN ('player', 'spectator')),
    joined_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (round_id, golfer_id),
    UNIQUE (id, round_id)
);

CREATE INDEX round_participants_round_idx ON round_participants(round_id);

CREATE TABLE round_hole_pars (
    round_id uuid NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
    hole_number smallint NOT NULL CHECK (hole_number BETWEEN 1 AND 18),
    par smallint NOT NULL CHECK (par BETWEEN 2 AND 7),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (round_id, hole_number)
);

CREATE TABLE round_hole_scores (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    round_id uuid NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
    hole_number smallint NOT NULL CHECK (hole_number BETWEEN 1 AND 18),
    score_scope varchar(16) NOT NULL CHECK (score_scope IN ('player', 'team')),
    player_participant_id uuid,
    strokes smallint NOT NULL CHECK (strokes BETWEEN 1 AND 99),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK (
        (score_scope = 'player' AND player_participant_id IS NOT NULL)
        OR (score_scope = 'team' AND player_participant_id IS NULL)
    ),
    FOREIGN KEY (player_participant_id, round_id)
        REFERENCES round_participants(id, round_id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX round_hole_player_score_unique
    ON round_hole_scores(round_id, hole_number, player_participant_id)
    WHERE score_scope = 'player';

CREATE UNIQUE INDEX round_hole_team_score_unique
    ON round_hole_scores(round_id, hole_number)
    WHERE score_scope = 'team';

CREATE TABLE round_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    round_id uuid NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
    actor_participant_id uuid,
    event_type varchar(48) NOT NULL CHECK (length(btrim(event_type)) > 0),
    hole_number smallint CHECK (hole_number BETWEEN 1 AND 18),
    old_value jsonb,
    new_value jsonb,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (actor_participant_id, round_id)
        REFERENCES round_participants(id, round_id) ON DELETE RESTRICT
);

CREATE INDEX round_events_round_time_idx
    ON round_events(round_id, created_at, id);

CREATE TABLE scramble_contributions (
    round_id uuid NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
    hole_number smallint NOT NULL CHECK (hole_number BETWEEN 1 AND 18),
    shot_type varchar(32) NOT NULL CHECK (length(btrim(shot_type)) BETWEEN 1 AND 32),
    player_participant_id uuid NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (round_id, hole_number, shot_type),
    FOREIGN KEY (player_participant_id, round_id)
        REFERENCES round_participants(id, round_id) ON DELETE CASCADE
);
