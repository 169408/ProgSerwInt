CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    number VARCHAR(20),
    city VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS offers (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    salary INT NOT NULL,
    location VARCHAR(255) NOT NULL,
    author_id UUID NOT NULL REFERENCES users(id), -- Foreign key to users table
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (id, name, email, password, number, city, created_at, updated_at)
VALUES
    (gen_random_uuid(),
    'John Doe',
    'john.doe@example.com',
    crypt('password123', gen_salt('bf')),
    '+12 345 678 920', 'New York',
    '2024-12-10 12:00:00',
    '2024-12-10 12:00:00'),

    (gen_random_uuid(),
    'Jane Smith',
    'jane.smith@example.com',
    crypt('securepass456', gen_salt('bf')),
    '0987654321',
    'Los Angeles',
    '2024-12-10 13:00:00',
    '2024-12-10 13:00:00');


WITH user_ids AS (
    SELECT id, name FROM users WHERE name IN ('John Doe', 'Jane Smith')
)
INSERT INTO offers (title, description, job_title, salary, location, author_id, created_at, updated_at)
SELECT
    'Junior Python Developer',
    'Looking for a junior developer skilled in Python and Django. Remote work possible.',
    'job_title1',
    4000,
    'New York',
    (SELECT id FROM user_ids WHERE name = 'John Doe'),
    '2024-12-10 14:00:00'::timestamp,
    '2024-12-10 14:00:00'::timestamp
UNION ALL
SELECT
    'Senior Data Scientist',
    'We are hiring a senior data scientist experienced in machine learning and big data.',
    'job_title2',
    12000,
    'San Francisco',
    (SELECT id FROM user_ids WHERE name = 'Jane Smith'),
    '2024-12-10 15:00:00'::timestamp,
    '2024-12-10 15:00:00'::timestamp
UNION ALL
SELECT
    'UI/UX Designer',
    'Creative UI/UX designer required to join a fast-growing startup.',
    'job_title3',
    5000,
    'Los Angeles',
    (SELECT id FROM user_ids WHERE name = 'John Doe'),
    '2024-12-10 16:00:00'::timestamp,
    '2024-12-10 16:00:00'::timestamp;

--INSERT INTO offers (title, description, salary, location, author_id, created_at, updated_at)
--VALUES
--    ('Junior Python Developer',
--     'Looking for a junior developer skilled in Python and Django. Remote work possible.',
--     4000,
--     'New York',
--     'c1a1c8be-6cbe-11ed-a1eb-0242ac120002',
--     '2024-12-10 14:00:00',
--     '2024-12-10 14:00:00'),
--
--    ('Senior Data Scientist',
--     'We are hiring a senior data scientist experienced in machine learning and big data.',
--     12000,
--     'San Francisco',
--     'c2b2d8cf-7dbe-11ed-b2fc-0242ac120003',
--     '2024-12-10 15:00:00',
--     '2024-12-10 15:00:00'),
--
--    ('UI/UX Designer',
--     'Creative UI/UX designer required to join a fast-growing startup.',
--     5000,
--     'Los Angeles',
--     'c1a1c8be-6cbe-11ed-a1eb-0242ac120002',
--     '2024-12-10 16:00:00',
--     '2024-12-10 16:00:00');