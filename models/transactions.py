import database


def select_all_transaction(user_id):
    results = database.sql_select(
        "SELECT value FROM transactions WHERE user_id = %s", [user_id])
    if len(results) > 0:
        return results[0]
    else:
        return None


def select_transaction(user_id, coin):
    results = database.sql_select(
        "SELECT value FROM transactions WHERE user_id = %s AND coin = %s;", [user_id, coin])
    if len(results) > 0:
        return results[0]
    else:
        return None


def insert_transaction(user_id, coin, value):
    database.sql_write("INSERT into transactions (user_id, coin, value) VALUES (%s, %s, %s);", [
        user_id,
        coin,
        value
    ])


def update_transaction(value, user_id, coin):
    database.sql_write("UPDATE transactions SET value = %s WHERE user_id = %s AND coin = %s;", [
                       value, user_id, coin])


def insert_history(user_id, history):
    database.sql_write("INSERT into history (user_id, history) VALUES (%s, %s);", [
        user_id,
        history])


def select_history(user_id):
    results = database.sql_select(
        "SELECT created_at, history FROM history WHERE user_id = %s ORDER BY created_at", [user_id])
    if len(results) > 0:
        return results
    else:
        return []
