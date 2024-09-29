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

const pieChartData = JSON.parse(document.getElementById('pieChartData').textContent);

// Extract the labels and data for the pie chart
const pieLabels = pieChartData[0].labels;
const pieData = pieChartData[1].data;

// Initialize the pie chart
const ctxPie = document.getElementById('pieChart').getContext('2d');
const pieChart = new Chart(ctxPie, {
    type: 'pie',  // Chart type is pie
    data: {
        labels: pieLabels,  // Pie chart labels
        datasets: [{
            label: 'Pie Data',
            data: pieData,  // Pie chart data
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});