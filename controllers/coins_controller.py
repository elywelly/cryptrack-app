from flask import Blueprint, session, request, redirect, render_template
import requests

coins_controller = Blueprint(
    "coins_controller", __name__, template_folder="../templates/coins")


@coins_controller.route('/coins')
def coins():
    coins = requests.get(
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=aud&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d')
    json = coins.json()
    return render_template('coins.html', coins=json)
