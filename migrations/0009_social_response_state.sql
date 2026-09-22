CREATE TABLE round_event_reactions (
    event_id uuid NOT NULL REFERENCES round_events(id) ON DELETE CASCADE,
    actor_participant_id uuid NOT NULL REFERENCES round_participants(id) ON DELETE CASCADE,
    reaction_kind varchar(24) NOT NULL
        CHECK (reaction_kind IN ('bullshit', 'cheater', 'lucky', 'nice', 'talk_shit')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (event_id, actor_participant_id)
);

CREATE INDEX round_event_reactions_actor_idx
    ON round_event_reactions(actor_participant_id, updated_at DESC);

CREATE TABLE score_challenges (
    score_event_id uuid NOT NULL REFERENCES round_events(id) ON DELETE CASCADE,
    challenger_participant_id uuid NOT NULL REFERENCES round_participants(id) ON DELETE CASCADE,
    proposed_score smallint CHECK (proposed_score BETWEEN 1 AND 99),
    comment text CHECK (comment IS NULL OR length(comment) <= 280),
    status varchar(16) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'withdrawn')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (score_event_id, challenger_participant_id),
    CHECK (proposed_score IS NOT NULL OR nullif(btrim(comment), '') IS NOT NULL)
);

CREATE INDEX score_challenges_status_idx
    ON score_challenges(score_event_id, status, updated_at DESC);
