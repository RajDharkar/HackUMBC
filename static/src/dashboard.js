// dashboard.js

// Get the embedded JSON data from the script tag
const barChartData = JSON.parse(document.getElementById('barChartData').textContent);

// Extract the X-axis labels and Y-axis data
const xLabels = barChartData[0].x_labels;
const yData = barChartData[1].y_data;

// Initialize the chart
const ctx = document.getElementById('barChart1').getContext('2d');

const barChart = new Chart(ctx, {
    type: 'bar',  // Chart type is bar
    data: {
        labels: xLabels,  // X-axis labels
        datasets: [{
            label: 'Sample Data',
            data: yData,  // Y-axis data
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
