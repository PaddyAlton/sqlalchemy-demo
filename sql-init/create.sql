-- creation of SQL tables

CREATE TABLE IF NOT EXISTS attendees (
  id SERIAL PRIMARY KEY,
  name VARCHAR(250) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

INSERT INTO attendees (name)
VALUES
  ('Paddy'),
  ('A'),
  ('B'),
  ('C'),
  ('D'),
  ('E')
  ;


INSERT INTO attendees (name)
VALUES
  ('F'),
  ('G'),
  ('H'),
  ('I'),
  ('J'),
  ('K')
  ;
