# CrypTrack App

Got too many crypto and exchanges to keep track of?
Create your own wallet to CrypTrack of all your Crypto values in one spot.

Vist it [here](https://floating-thicket-31159.herokuapp.com/)

# Planning

## What information do I need?

-   API for Crypto data (CoinGecko)
-   Database for user logins and passwords
-   Database to hold user wallet values for each crypto
-   Homepage with Top 100 data
-   Wallet page for users to view (Total amount in Fiat and individual Crypto)
-   Transaction page to create new Transactions

## Layout Plans

### Changes Made

-   Created an additional database for history, linked to user id to capture user's transaction history

![Flow with database](https://github.com/elywelly/cryptrack-app/blob/main/static/Flowchart.png?raw=true)
![Pages needed](https://github.com/elywelly/cryptrack-app/blob/main/static/pages.png?raw=true)

## Functions Breakdown

-   Users are able to view Top 100 Crypto Data from the homepage
-   User to sign up or login (if password matches database)
-   Upon logging in, user will have access to Wallet and Transactions page
-   Wallet page will display user's total wallet amount in AUD and list each Crypto held
-   Transactions allow user to add a new transaction
-   New transaction starts by checking if the crypto symbol matches/is supported with AUD (through API call)
-   If supported, user will be able to choose between "buy" or "sell" to add to their wallet and the amount
-   Database to update based on user's ID and the value of particular crypto held
-   Insert history message for each transaction to display in transaction history
-   Wallet will be updated based on sum of all crypto in AUD.
