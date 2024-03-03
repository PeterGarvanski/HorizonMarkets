// Get the canvas element
var chartElement = document.getElementById('account-history-chart');
var accountData = chartElement.getAttribute('my-data');
var ctx = chartElement.getContext('2d');

// Define the data
var data = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
  datasets: [{
    label: 'Account Value',
    backgroundColor: '#69A2E0',
    borderColor: '#437DBC',
    data: accountData.split(','),
  }]
};

// Configure the chart
var myChart = new Chart(ctx, {
  type: 'line',
  data: data,
  options: {
    scales: {
      x: {
        grid: {
          color: '#437dbc3b' // Specify the color for the x-axis grid lines
        },
        ticks: {
          color: '#080B0E' // Specify the color for the x-axis ticks
        }
      },
      y: {
        grid: {
          color: '#437dbc3b' // Specify the color for the y-axis grid lines
        },
        ticks: {
          color: '#080B0E' // Specify the color for the y-axis ticks
        }
      }
    }
  }
});