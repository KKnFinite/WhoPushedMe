ALTER TABLE rounds
    ADD COLUMN current_route_position integer NOT NULL DEFAULT 1
        CHECK (current_route_position >= 1),
    ADD COLUMN par_tracking_enabled boolean NOT NULL DEFAULT true,
    ADD COLUMN end_reason varchar(24)
        CHECK (end_reason IS NULL OR end_reason IN ('normal', 'ended_early'));

CREATE TABLE round_route_positions (
    round_id uuid NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
    route_position integer NOT NULL CHECK (route_position >= 1),
    hole_number smallint NOT NULL CHECK (hole_number BETWEEN 1 AND 18),
    state varchar(16) NOT NULL DEFAULT 'planned'
        CHECK (state IN ('planned', 'skipped')),
    skip_reason text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (round_id, route_position),
    CHECK (
        (state = 'planned' AND skip_reason IS NULL)
        OR state = 'skipped'
    )
);

INSERT INTO round_route_positions (
    round_id,
    route_position,
    hole_number
)
SELECT
    r.id,
    generated.route_position,
    generated.route_position::smallint
FROM rounds r
CROSS JOIN LATERAL generate_series(
    1,
    r.hole_count
) AS generated(route_position);

ALTER TABLE round_hole_scores
    ADD COLUMN route_position integer;

UPDATE round_hole_scores
SET route_position = hole_number;

ALTER TABLE round_hole_scores
    ALTER COLUMN route_position SET NOT NULL,
    ADD CONSTRAINT round_hole_scores_route_fk
        FOREIGN KEY (round_id, route_position)
        REFERENCES round_route_positions(round_id, route_position)
        ON DELETE CASCADE;

DROP INDEX round_hole_player_score_unique;
DROP INDEX round_hole_team_score_unique;

CREATE UNIQUE INDEX round_route_player_score_unique
    ON round_hole_scores(round_id, route_position, player_participant_id)
    WHERE score_scope = 'player';

CREATE UNIQUE INDEX round_route_team_score_unique
    ON round_hole_scores(round_id, route_position)
    WHERE score_scope = 'team';

ALTER TABLE scramble_contributions
    ADD COLUMN route_position integer;

UPDATE scramble_contributions
SET route_position = hole_number;

ALTER TABLE scramble_contributions
    ALTER COLUMN route_position SET NOT NULL,
    ADD CONSTRAINT scramble_contributions_route_fk
        FOREIGN KEY (round_id, route_position)
        REFERENCES round_route_positions(round_id, route_position)
        ON DELETE CASCADE;

ALTER TABLE scramble_contributions
    DROP CONSTRAINT scramble_contributions_pkey;

ALTER TABLE scramble_contributions
    ADD PRIMARY KEY (round_id, route_position, shot_type);

ALTER TABLE round_events
    ADD COLUMN route_position integer;

UPDATE round_events
SET route_position = hole_number
WHERE hole_number IS NOT NULL;

ALTER TABLE round_events
    ADD CONSTRAINT round_events_route_fk
        FOREIGN KEY (round_id, route_position)
        REFERENCES round_route_positions(round_id, route_position);

CREATE INDEX round_events_route_idx
    ON round_events(round_id, route_position, created_at, id)
    WHERE route_position IS NOT NULL;

CREATE TABLE round_route_pars (
    round_id uuid NOT NULL,
    route_position integer NOT NULL,
    par smallint NOT NULL CHECK (par BETWEEN 2 AND 7),
    source varchar(16) NOT NULL DEFAULT 'course'
        CHECK (source IN ('course', 'manual', 'assumed')),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (round_id, route_position),
    FOREIGN KEY (round_id, route_position)
        REFERENCES round_route_positions(round_id, route_position)
        ON DELETE CASCADE
);

INSERT INTO round_route_pars (
    round_id,
    route_position,
    par,
    source
)
SELECT
    route.round_id,
    route.route_position,
    pars.par,
    'course'
FROM round_route_positions route
JOIN round_hole_pars pars
  ON pars.round_id = route.round_id
 AND pars.hole_number = route.hole_number;

ALTER TABLE round_participants
    ADD COLUMN participation_state varchar(24) NOT NULL DEFAULT 'active'
        CHECK (participation_state IN ('active', 'withdrew', 'removed')),
    ADD COLUMN tracked_from_position integer NOT NULL DEFAULT 1
        CHECK (tracked_from_position >= 1);

CREATE TABLE round_participant_route_positions (
    round_id uuid NOT NULL,
    participant_id uuid NOT NULL,
    route_position integer NOT NULL,
    required boolean NOT NULL DEFAULT true,
    added_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (participant_id, route_position),
    FOREIGN KEY (participant_id, round_id)
        REFERENCES round_participants(id, round_id)
        ON DELETE CASCADE,
    FOREIGN KEY (round_id, route_position)
        REFERENCES round_route_positions(round_id, route_position)
        ON DELETE CASCADE
);

INSERT INTO round_participant_route_positions (
    round_id,
    participant_id,
    route_position,
    required
)
SELECT
    rp.round_id,
    rp.id,
    route.route_position,
    true
FROM round_participants rp
JOIN round_route_positions route
  ON route.round_id = rp.round_id
WHERE rp.role = 'player';
