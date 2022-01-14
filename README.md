# CrypTrack App

Create your own wallet to CrypTrack of all your Crypto Prices in one spot. (Amounts are all in AUD)

Vist it [here](https://floating-thicket-31159.herokuapp.com/)

# Planning

## What information do I need?

-   API for Crypto data (CoinGecko)
-   Database for user logins and passwords
-   Database to hold user wallet values
-   Homepage with Top 100 data
-   Wallet page for users to view
-   Transaction page to create new Transactions

## Layout Plans

![Flow with database](https://github.com/elywelly/cryptrack-app/blob/main/static/Flowchart.png?raw=true)
![Pages needed](https://github.com/elywelly/cryptrack-app/blob/main/static/pages.png?raw=true)

## Functions Breakdown

-   Users are able to view Top 100 Crypto Data from the homepage
-   User to sign up or login
-   Upon logging in, user will have access to Wallet and Transactions page
-   Wallet page will display user's total wallet amount in AUD and list each Crypto held
-   Transactions allow user to add a new transaction
-   New transaction starts by checking if the crypto symbol matches/is supported with AUD
-   If supported, user will be able to choose between "buy" or "sell" to add to their wallet and the amount
-   Database to update based on user's ID and the value of particular crypto held
-   Insert additional History message to display transaction history
-   Wallet will be updated based on sum of all crypto in AUD.
