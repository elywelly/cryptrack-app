from flask import Blueprint, session, request, redirect, render_template
import requests
from models.transactions import select_transaction, insert_transaction, insert_history, update_transaction, select_history, select_all_transaction, delete_history, delete_wallet

coins_controller = Blueprint(
    "coins_controller", __name__, template_folder="../templates/coins")


@coins_controller.route('/coins', methods=['GET'])
def coins():

    sort = request.values.get('sort')
    sort_type = "market_cap_"
    sort_by = "desc"
    message = "TOP"
    if sort != None:
        if sort == "MCASC":
            sort_type = "market_cap_"
            sort_by = "asc"
            message = "BOTTOM"
        elif sort == "MCDESC":
            sort_type = "market_cap_"
            sort_by = "desc"
            message = "TOP"
        elif sort == "PASC":
            sort_type = "price_"
            sort_by = "asc"
            message = "BOTTOM"
        elif sort == "PADESC":
            sort_type = "price_"
            sort_by = "desc"
            message = "TOP"

    currency = request.values.get('currency')
    current_currency = "AUD"
    if currency == None:
        currency = "aud"
        current_currency = currency.upper()
    else:
        currency = request.values.get('currency')
        current_currency = currency.upper()

    coins = requests.get(
        f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&order={sort_type}{sort_by}&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d')

    json = coins.json()

    return render_template('coins.html', coins=json, message=message, current_currency=current_currency)


@coins_controller.route('/coins/search', methods=['GET', 'POST'])
def search():

    currency = request.values.get('currency')
    current_currency = "AUD"
    if currency == None:
        currency = "aud"
        current_currency = currency.upper()
    else:
        currency = request.values.get('currency')
        current_currency = currency.upper()

    # check coins
    coins = requests.get(
        f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&order=asc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d')
    json = coins.json()
    coin_search = request.form.get("search")

    if coin_search == None:
        return redirect('/')

    for i in range(len(json)):
        if coin_search.lower() == json[i]['symbol'] or coin_search.lower() == json[i]['id']:
            return render_template('coin-search.html', coin=json[i], current_currency=current_currency, coin_search=coin_search)

    return render_template('coin-search.html', coin=json[i], coin_search=coin_search, current_currency=current_currency, no_results="Coin not found or supported. Please ensure you are using the coin's symbol or name.")


@coins_controller.route('/coins/transactions')
def transactions():
    if not session.get('user_id'):
        return redirect('/login')

    user_id = session.get('user_id')

    all_history = select_history(user_id)
    return render_template('transactions.html', history=all_history)


@coins_controller.route('/coins/transactions', methods=["POST"])
def find_coin():
    if not session.get('user_id'):
        return redirect('/login')

    # history
    user_id = session.get('user_id')
    all_history = select_history(user_id)

    # check coins
    coins = requests.get(
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=aud&order=market_cap_desc&per_page=250&page=1&sparkline=false')
    json = coins.json()
    coin_name = request.form.get("name")

    for i in range(len(json)):
        if coin_name.lower() == json[i]['symbol'] or coin_name.lower() == json[i]['id']:
            # insert history here and return with link to wallet
            return render_template('coin-transaction.html', coin=json[i], history=all_history)

    return render_template('transactions.html', history=all_history, message="Coin not found or supported. Please ensure you are using the coin's name (e.g. Bitcoin) or symbol (e.g. BTC).")


@ coins_controller.route('/coins/transactions/history', methods=["GET", "POST"])
def delete_transactions():

    delete = request.form.get("delete")

    if delete == None:
        return redirect('/coins')

    if delete == 'Delete History':
        user_id = int(session.get('user_id'))
        delete_history(user_id)
        return redirect('/coins/transactions')

    return redirect('/')


@ coins_controller.route('/coins/transactions/coin', methods=["GET", "POST"])
def coin_transaction():
    if not session.get('user_id'):
        return redirect('/login')

    delete = request.form.get("delete")
    if delete == None:
        pass

    user_id = int(session.get('user_id'))
    coin = request.form.get("name")
    value = request.form.get("value")
    transaction = request.form.get("transactions")
    current_price = request.form.get("current_price")

    if value == None:
        return redirect('/coins/transactions')

    value = float(value)

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
            return redirect('/coins/wallet')

        # if found, update value by adding to it
        else:
            # add new history
            history = f"Bought {value} {coin} at {current_price}"
            insert_history(user_id, history)

            # update value in db
            new_value = 0
            new_value = float(coin_select[0]) + value
            update_transaction(new_value, user_id, coin)
            return redirect('/coins/wallet')

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
                return redirect('/coins/wallet')

    return redirect('/')


@ coins_controller.route('/coins/wallet/empty', methods=["GET", "POST"])
def empty_wallet():

    empty = request.form.get("delete")

    if empty == None:
        return redirect('/coins/wallet')

    if empty == 'Empty Wallet':
        user_id = int(session.get('user_id'))
        delete_wallet(user_id)
        return redirect('/coins/wallet')

    return redirect('/')


@ coins_controller.route('/coins/wallet', methods=['GET'])
def wallet():
    if not session.get('user_id'):
        return redirect('/login')

    empty = request.form.get("delete")
    if empty == None:
        pass

    currency = request.values.get('currency')
    current_currency = "AUD"
    if currency == None:
        currency = "aud"
        current_currency = currency.upper()
    else:
        currency = request.values.get('currency')
        current_currency = currency.upper()

    user_id = session.get('user_id')
    coins_held = select_all_transaction(user_id)

    # User total wallet value in fiat
    amount = 0

    # to check each crypto price in fiat
    coins = requests.get(
        f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&order=market_cap_desc&per_page=250&page=1&sparkline=false')
    json = coins.json()

    for coin in json:
        for each_coin in coins_held:
            if each_coin[1] == coin["symbol"]:
                # fiat value for each coin
                coin_fiat = float(each_coin[0]) * float(coin["current_price"])
                amount += coin_fiat

    return render_template('wallet.html', amount=amount, coins_held=coins_held, list=json, current_currency=current_currency)
