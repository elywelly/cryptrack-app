// Delete history 2
const historyDelete = document.querySelector('#history-delete');

historyDelete.addEventListener('click', function (event) {
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
