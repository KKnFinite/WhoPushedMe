ALTER TABLE round_participants
    ADD COLUMN tee_name text
        CHECK (tee_name IS NULL OR length(btrim(tee_name)) BETWEEN 1 AND 40);
