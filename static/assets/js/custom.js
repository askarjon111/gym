document.getElementById('id_plan').addEventListener('change', function () {
    var planId = document.getElementById('id_plan').value;
    if (planId) {
        updateEndDate(planId);
    }
});

function updateEndDate(planId) {
    const baseUrl = window.location.host;
    const apiUrl = 'http://' + baseUrl + `/plans/${planId}/days/`
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
            var planId = document.getElementById('id_plan').value;

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