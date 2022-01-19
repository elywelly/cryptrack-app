// Check before deleting account
const deleteAccount = document.querySelector('#delete-account');

deleteAccount.addEventListener('click', function (event) {
    if (
        confirm(
            'Are you sure you want to delete account? All information will be deleted. This cannot be undone.'
        )
    ) {
        pass;
    } else {
        event.preventDefault();
    }
});
