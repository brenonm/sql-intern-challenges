SET search_path TO case1;

CREATE TABLE users (
  user_id          INT PRIMARY KEY,
  created_at       DATE NOT NULL,
  country          TEXT NOT NULL,
  marketing_source TEXT NOT NULL
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  category   TEXT NOT NULL,
  brand      TEXT NOT NULL,
  cost       NUMERIC(10,2) NOT NULL
);

CREATE TABLE subscriptions (
  subscription_id INT PRIMARY KEY,
  user_id         INT NOT NULL REFERENCES users(user_id),
  plan            TEXT NOT NULL,
  start_date      DATE NOT NULL,
  end_date        DATE,
  status          TEXT NOT NULL
);

CREATE TABLE orders (
  order_id    INT PRIMARY KEY,
  user_id     INT NOT NULL REFERENCES users(user_id),
  order_date  DATE NOT NULL,
  status      TEXT NOT NULL,
  channel     TEXT NOT NULL
);

CREATE TABLE order_items (
  order_id    INT NOT NULL REFERENCES orders(order_id),
  product_id  INT NOT NULL REFERENCES products(product_id),
  qty         INT NOT NULL,
  unit_price  NUMERIC(10,2) NOT NULL,
  PRIMARY KEY (order_id, product_id)
);

CREATE TABLE returns (
  return_id    INT PRIMARY KEY,
  order_id     INT NOT NULL REFERENCES orders(order_id),
  product_id   INT NOT NULL REFERENCES products(product_id),
  qty          INT NOT NULL,
  return_date  DATE NOT NULL,
  reason       TEXT NOT NULL
);

CREATE TABLE campaign_attribution (
  user_id     INT NOT NULL REFERENCES users(user_id),
  campaign_id INT NOT NULL,
  touched_at  DATE NOT NULL
);