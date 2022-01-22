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

// to update details
const username = document.querySelector('#to-update-name');

username.addEventListener('click', function () {
    document.querySelector('#update-name').classList.remove('hidden');
});

const email = document.querySelector('#to-update-email');

email.addEventListener('click', function () {
    document.querySelector('#update-email').classList.remove('hidden');
});

const password = document.querySelector('#to-update-password');

password.addEventListener('click', function () {
    document.querySelector('#update-password').classList.remove('hidden');
});
