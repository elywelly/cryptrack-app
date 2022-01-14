from flask import Blueprint, session, request, redirect, render_template
import requests
from models.transactions import select_transaction, insert_transaction, insert_history, update_transaction, select_all_transaction

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

    # display transaction history - include in jinja to display
    user_id = session.get('user_id')
    select_all_transaction(user_id)

    return render_template('transactions.html')


@coins_controller.route('/coins/transactions', methods=["POST"])
def find_coin():
    if not session.get('user_id'):
        return redirect('/login')

    # check if coin exists
    coins = requests.get(
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=aud&order=market_cap_desc&per_page=250&page=1&sparkline=false')
    json = coins.json()
    coin_name = request.form.get("name")
    for coin in json:
        if coin_name.lower() != coin['symbol']:
            return render_template('transactions.html', message="Coin not found or supported. Please ensure you are using the coin's symbol (e.g. BTC).")
        else:
            # only works for btc
            # insert history here and return with link to wallet
            return render_template('coin-transaction.html', coin=coin)


@ coins_controller.route('/coins/transactions/<coin>', methods=["POST"])
def coin_transaction(coin):
    user_id = session.get('user_id')
    coin = coin  # get coin selected
    value = request.form.get("value")
    transaction = request.form.get("transaction")

    if transaction == "buy":

        # get data from database
        coin_select = select_transaction(user_id, coin)

        # if none, insert
        if coin_select == None:

            # to insert current price. another API call?
            history = f"Bought {value} {coin} at "
            insert_transaction(user_id, coin, value, history)
            redirect("/coins/transactions")

        # if found, update value by adding to it
        else:
            # add new history
            history = f"Bought {value} {coin} at "
            insert_history(history, user_id, coin)

            # update value in db
            new_value = coin_select[0] + value
            update_transaction(new_value, user_id, coin)
            redirect("/coins/transactions")

    if transaction == "sell":

        # get data from database
        coin_select = select_transaction(user_id, coin)

        # error
        if coin_select == None:
            render_template("transactions.html",
                            message="You do not have this coin in your wallet")

        # if found, update value by adding to it
        else:
            history = f"Sold {value} {coin} at "
            insert_history(history, user_id, coin)

            new_value = coin_select[0] - value
            update_transaction(new_value, user_id, coin)
            redirect("/coins/transactions")


@ coins_controller.route('/coins/wallet')
def wallet():
    return render_template('wallet.html')
