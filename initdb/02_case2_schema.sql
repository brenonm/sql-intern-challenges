SET search_path TO case2;

CREATE TABLE accounts (
  account_id INT PRIMARY KEY,
  name       TEXT NOT NULL,
  created_at DATE NOT NULL,
  tier       TEXT NOT NULL
);

CREATE TABLE app_users (
  user_id    INT PRIMARY KEY,
  account_id INT NOT NULL REFERENCES accounts(account_id),
  created_at DATE NOT NULL,
  role       TEXT NOT NULL
);

CREATE TABLE events (
  event_id        BIGINT PRIMARY KEY,
  user_id         INT NOT NULL REFERENCES app_users(user_id),
  event_ts        TIMESTAMP NOT NULL,
  event_type      TEXT NOT NULL,
  page            TEXT NOT NULL,
  session_id      TEXT NOT NULL,
  properties_jsonb JSONB NOT NULL
);

CREATE TABLE tickets (
  ticket_id   INT PRIMARY KEY,
  account_id  INT NOT NULL REFERENCES accounts(account_id),
  created_at  DATE NOT NULL,
  status      TEXT NOT NULL,
  priority    TEXT NOT NULL,
  closed_at   DATE
);

CREATE TABLE ticket_events (
  ticket_id     INT NOT NULL REFERENCES tickets(ticket_id),
  event_ts      TIMESTAMP NOT NULL,
  new_status    TEXT NOT NULL,
  actor_user_id INT NOT NULL REFERENCES app_users(user_id)
);