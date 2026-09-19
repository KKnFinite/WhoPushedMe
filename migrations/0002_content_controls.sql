CREATE TABLE golfer_content_preferences (
    golfer_id uuid PRIMARY KEY REFERENCES golfers(id) ON DELETE CASCADE,
    mini_mascots_enabled boolean NOT NULL DEFAULT true,
    trash_talk_enabled boolean NOT NULL DEFAULT true,
    max_vulgarity varchar(16) NOT NULL DEFAULT 'normal'
        CHECK (max_vulgarity IN ('normal', 'brutal')),
    theme_preferences jsonb NOT NULL DEFAULT '{}'::jsonb
        CHECK (jsonb_typeof(theme_preferences) = 'object'),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE content_system_settings (
    singleton boolean PRIMARY KEY DEFAULT true CHECK (singleton),
    mini_mascots_enabled boolean NOT NULL DEFAULT true,
    trash_talk_enabled boolean NOT NULL DEFAULT true,
    updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO content_system_settings (singleton)
VALUES (true)
ON CONFLICT (singleton) DO NOTHING;

CREATE TABLE content_event_overrides (
    event_key text PRIMARY KEY CHECK (length(btrim(event_key)) > 0),
    enabled boolean NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);
