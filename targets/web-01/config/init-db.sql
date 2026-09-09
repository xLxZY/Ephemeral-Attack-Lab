CREATE USER acme WITH PASSWORD 'acme_lab_db';
CREATE DATABASE acme_reporting OWNER acme;
\connect acme_reporting
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
INSERT INTO reports (title) VALUES
    ('Weekly pipeline status'),
    ('Customer cohort snapshot');
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO acme;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO acme;
