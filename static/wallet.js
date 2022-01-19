// Empty Wallet
const emptyWallet = document.querySelector('#emptyWallet');

emptyWallet.addEventListener('click', function (event) {
    if (
        confirm(
            'Are you sure you want to empty wallet? All coins in your wallet will be deleted. This cannot be undone.'
        )
    ) {
        pass;
    } else {
        event.preventDefault();
    }
});
