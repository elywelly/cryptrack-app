# CrypTrack App

Got too many crypto and exchanges to keep track of?
Create your own wallet to CrypTrack of all your Crypto values in one spot.

Vist it [here](https://floating-thicket-31159.herokuapp.com/)

## Tech Used

-   HTML/CSS
-   Python
-   Flask
-   Jinja
-   PostgreSQL

## Planning

### What information do I need?

-   API for Crypto data (CoinGecko)
-   Database for user logins and passwords
-   Database to hold user wallet values for each crypto
-   Homepage with Top 100 data
-   Wallet page for users to view (Total amount in Fiat and individual Crypto)
-   Transaction page to create new Transactions

### Layout Plans

#### Changes Made

-   Created an additional database for history, linked to user id to capture user's transaction history
-   Added a search bar to page under navigation
-   Request user to select coin first before starting transaction with information on coin selected
-   No individual coin data page yet with more info

![Flow with database](https://github.com/elywelly/cryptrack-app/blob/main/static/Flowchart.png?raw=true)
![Pages needed](https://github.com/elywelly/cryptrack-app/blob/main/static/pages.png?raw=true)

## Functions Breakdown

-   Users are able to view Top 100 Crypto Data from the homepage
    -   API data display
-   User to sign up or login (if password matches users database)
    -   To match database (password to be encrypted)
-   Upon logging in, user will have access to Wallet and Transactions page
-   Wallet page will display user's total wallet amount in Fiat and list each Crypto held
    -   API call for current price to calculate updated amount of each crypto (from transactions database)
    -   Update total wallet value in Fiat from crypto held (from transactions database)
-   Transactions to allow user to add a new transaction
-   New transaction starts by checking if the crypto symbol matches/is supported with Fiat currency (through API call)
-   If supported, user will be able to choose between "buy" or "sell" to add to their wallet and the amount
-   Transactions batabase to update based on user's ID and the value of particular crypto held
-   Insert history message to history database for each transaction to display in transaction history
-   Wallet will be updated based on sum of all crypto

## Further Developments

-   Added About page
-   Added currency options (to coins and wallet)
-   Ability to sort by Market Price or Current Price for coins
-   Add search function for coin by crypto name or symbol
-   Ability for user to delete their transaction history (in progress)
-   Transactions Database to delete coins that have 0 value so it doesn't appear in wallet

## Credits

Coin API data from [CoinGecko](https://www.coingecko.com/en/api/documentation)
