-- Users
CREATE TABLE users(id SERIAL PRIMARY KEY, email text NOT NULL, name text NOT NULL, password text NOT NULL);
ALTER TABLE users ADD CONSTRAINT email_unique UNIQUE(email);

-- Transactions

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    coin TEXT,
    value INTEGER,
    history VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user
      FOREIGN KEY(user_id)
	  REFERENCES users(id)
);