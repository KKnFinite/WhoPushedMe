ALTER TABLE golfers
ADD COLUMN spouse_type varchar(16)
    CHECK (spouse_type IN ('wife', 'husband', 'not_married'));
