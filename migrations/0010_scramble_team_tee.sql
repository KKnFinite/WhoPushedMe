ALTER TABLE rounds
    ADD COLUMN scramble_tee_name text
        CHECK (
            scramble_tee_name IS NULL
            OR length(btrim(scramble_tee_name)) BETWEEN 1 AND 40
        );

UPDATE rounds r
SET scramble_tee_name = existing.tee_name
FROM LATERAL (
    SELECT rp.tee_name
    FROM round_participants rp
    WHERE rp.round_id = r.id
      AND rp.role = 'player'
      AND rp.tee_name IS NOT NULL
    ORDER BY rp.joined_at, rp.id
    LIMIT 1
) existing
WHERE r.mode = 'scramble';

UPDATE round_participants rp
SET tee_name = NULL
FROM rounds r
WHERE r.id = rp.round_id
  AND r.mode = 'scramble'
  AND rp.role = 'player';
