document.getElementById('id_plan').addEventListener('change', function () {
    var planId = document.getElementById('id_plan').value;
    if (planId) {
        updateEndDate(planId);
    }
});

function updateEndDate(planId) {
    const baseUrl = window.location.host;
    var apiUrl = 'http://' + baseUrl + `/dashboard/plans/${planId}/days/`
    if (!baseUrl.includes('127.0.0.1')) {
        apiUrl = 'https://' + baseUrl + `/dashboard/plans/${planId}/days/`
    }

    const options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
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

            if (data.days !== null) {
                var startDate = new Date(document.getElementById('id_start_date').value);
                var endDate = new Date(startDate.getTime() + data.days * 24 * 60 * 60 * 1000);
                var endDateFormat = endDate.getFullYear() + '-' + (endDate.getMonth() + 1).toString().padStart(2, '0') + '-' + endDate.getDate().toString().padStart(2, '0');
                document.getElementById('id_end_date').value = endDateFormat;
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}
const cancelButtonList = document.querySelectorAll('.cancel-subscription');

cancelButtonList.forEach(function (cancelButton) {
    cancelButton.addEventListener('click', function (event) {
        event.preventDefault();

        const buttonValue = this.value
        cancelSubscription(buttonValue);
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

function cancelSubscription(subId) {
    const csrftoken = getCookie('csrftoken');

    const baseUrl = window.location.host;
    const url = '/dashboard/subscriptions/' + subId + '/cancel/'
    var apiUrl = 'http://' + baseUrl + url;
    if (!baseUrl.includes('127.0.0.1')) {
        apiUrl = 'https://' + baseUrl + url;
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
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}
