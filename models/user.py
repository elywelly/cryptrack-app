import database


def insert_user(email, name, hashed_password):
    database.sql_write(
        'INSERT INTO users (email, name, password) VALUES (%s, %s, %s);', [email, name, hashed_password])


def get_user_by_email(email):
    results = database.sql_select(
        "SELECT * FROM users WHERE email = %s", [email])
    if len(results) > 0:
        return results[0]
    else:
        return None


def delete_user(user_id):
    database.sql_write(
        "DELETE FROM users WHERE id = %s", [user_id])
