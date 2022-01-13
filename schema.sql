-- Users

CREATE TABLE users(id SERIAL PRIMARY KEY, email text NOT NULL, name text NOT NULL, password text NOT NULL);

-- Transactions

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    coin TEXT,
    transaction_amount INTEGER,
    transaction_type text,
    CONSTRAINT fk_user
      FOREIGN KEY(user_id)
	  REFERENCES users(id)
);