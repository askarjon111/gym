document.addEventListener("DOMContentLoaded", function () {
    const cancelButtonList = document.querySelectorAll('.cancel-subscription');

    cancelButtonList.forEach(function (cancelButton) {
        cancelButton.addEventListener('click', function (event) {
            event.preventDefault();

            if (this.classList.contains('disabled')) return; // Prevent multiple clicks

            this.disabled = true;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>'; // Show loading spinner

            const buttonValue = this.value;
            cancelSubscription(buttonValue, this);
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function cancelSubscription(subId, button) {
    const csrftoken = getCookie('csrftoken');

    const baseUrl = window.location.host;
    const url = `/gym/subscriptions/${subId}/cancel/`;
    var apiUrl = `http://${baseUrl}${url}`;
    if (!baseUrl.includes('127.0.0.1')) {
        apiUrl = `https://${baseUrl}${url}`;
    }

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    };

    fetch(apiUrl, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Successfully canceled subscription
            button.innerHTML = '<i class="fas fa-cancel"></i>'; // Show success icon
            button.classList.add('disabled'); // Disable button permanently
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            button.disabled = false;  // Re-enable button if request fails
            button.innerHTML = '<i class="fas fa-cancel"></i>'; // Restore icon
        });
}