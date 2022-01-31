-- Users
CREATE TABLE users(
  id SERIAL PRIMARY KEY, 
  email text NOT NULL unique, 
  name VARCHAR(255) NOT NULL, 
  password VARCHAR(64) NOT NULL
  );

-- Transactions

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    coin VARCHAR(10),
    value NUMERIC,
    CONSTRAINT fk_user
      FOREIGN KEY(user_id)
	  REFERENCES users(id)
);

-- History

CREATE TABLE history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    history VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user
      FOREIGN KEY(user_id)
	  REFERENCES users(id)
);