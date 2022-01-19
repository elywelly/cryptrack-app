// Delete history 1
const deleteHistory = document.querySelector('#delete-history');

deleteHistory.addEventListener('click', function (event) {
    if (
        confirm(
            'Are you sure you want to delete all history? This cannot be undone.'
        )
    ) {
        pass;
    } else {
        event.preventDefault();
    }
});
