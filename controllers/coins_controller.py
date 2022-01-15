from flask import Blueprint, session, request, redirect, render_template
import requests
from models.transactions import select_transaction, insert_transaction, insert_history, update_transaction, select_all_transaction, select_history

coins_controller = Blueprint(
    "coins_controller", __name__, template_folder="../templates/coins")


@coins_controller.route('/coins')
def coins():
    coins = requests.get(
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=aud&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d')
    json = coins.json()
    return render_template('coins.html', coins=json)


@coins_controller.route('/coins/transactions')
def transactions():
    if not session.get('user_id'):
        return redirect('/login')

    user_id = session.get('user_id')
    select_all_transaction(user_id)

    all_history = select_history(user_id)
    return render_template('transactions.html', history=all_history)


@coins_controller.route('/coins/transactions', methods=["POST"])
def find_coin():
    if not session.get('user_id'):
        return redirect('/login')

    # history
    user_id = session.get('user_id')
    all_history = select_history(user_id)

    coins = requests.get(
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=aud&order=market_cap_desc&per_page=250&page=1&sparkline=false')
    json = coins.json()
    coin_name = request.form.get("name")
    for i in range(len(json)):
        if coin_name.lower() == json[i]['symbol']:
            # insert history here and return with link to wallet
            return render_template('coin-transaction.html', coin=json[i], history=all_history)

    return render_template('transactions.html', history=all_history, message="Coin not found or supported. Please ensure you are using the coin's symbol (e.g. BTC).")


@ coins_controller.route('/coins/transactions/coin', methods=["POST"])
def coin_transaction():
    if not session.get('user_id'):
        return redirect('/login')
    user_id = int(session.get('user_id'))
    coin = request.form.get("name")
    value = float(request.form.get("value"))
    transaction = request.form.get("transactions")
    current_price = request.form.get("current_price")

    # history
    user_id = session.get('user_id')
    all_history = select_history(user_id)

    if transaction == "buy":

        # get data from database
        coin_select = select_transaction(user_id, coin)

        # if none, insert
        if coin_select == None:

            history = f"Bought {value} {coin} at {current_price}"
            insert_history(user_id, history)
            insert_transaction(user_id, coin, value)
            return render_template("transactions.html", success=f"Transaction successfully added to wallet. Refresh for updated history", history=all_history)

        # if found, update value by adding to it
        else:
            # add new history
            history = f"Bought {value} {coin} at {current_price}"
            insert_history(user_id, history)

            # update value in db
            new_value = 0
            new_value = float(coin_select[0]) + value
            update_transaction(new_value, user_id, coin)
            return render_template("transactions.html", success=f"Transaction successfully added to wallet. Refresh for updated history", history=all_history)

    if transaction == "sell":

        # get data from database
        coin_select = select_transaction(user_id, coin)

        # error
        if coin_select == None:
            return render_template("transactions.html",
                                   message="You do not have this coin in your wallet", history=all_history)

        # if found, update value by taking away from it
        else:
            new_value = 0
            new_value = float(coin_select[0]) - value

            # check if it is more than the user has
            if new_value < 0:
                return render_template("transactions.html", message=f"You do not have enough {coin.upper()}", history=all_history)
            else:
                history = f"Sold {value} {coin} at {current_price}"
                insert_history(user_id, history)
                update_transaction(new_value, user_id, coin)
                return render_template("transactions.html", success=f"Transaction successfully added to wallet. Refresh for updated history", history=all_history)


@ coins_controller.route('/coins/wallet')
def wallet():
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('wallet.html')
