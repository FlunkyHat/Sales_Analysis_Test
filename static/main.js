// Fetch the data from the Flask routes
fetch('/monthly_summary_data')
    .then(response => response.json())
    .then(data => {
        // Create the monthly summary chart
        new Chart(document.getElementById('monthlySummaryChart'), {
            type: 'bar',
            data: {
                labels: data.months,
                datasets: [{
                    label: 'Total Sales Value',
                    data: data.total_sales_values,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }, {
                    label: 'Number of Calls',
                    data: data.number_of_calls,
                    backgroundColor: 'rgba(255, 206, 86, 0.2)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 1
                }, {
                    label: 'Average Value',
                    data: data.average_values,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }, {
                    label: 'Median Value',
                    data: data.median_values,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    });

fetch('/advisor_summary_data')
    .then(response => response.json())
    .then(data => {
        // Create the advisor summary chart
        new Chart(document.getElementById('advisorSummaryChart'), {
            type: 'line',
            data: {
                labels: data.months,
                datasets: data.advisors.map((advisor, index) => ({
                    label: advisor.name,
                    data: advisor.total_sales_values,
                    fill: false,
                    borderColor: `hsl(${(index * (360 / data.advisors.length))}, 50%, 50%)`,
                    lineTension: 0.1
                }))
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    });
