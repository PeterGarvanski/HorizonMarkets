// Get the canvas element
var ctx = document.getElementById('account-history-chart').getContext('2d');

// Define the data
var data = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
  datasets: [{
    label: 'Account Value',
    backgroundColor: '#69A2E0',
    borderColor: '#437DBC',
    data: [50000, 45789, 36789, 42516, 52456, 59123, 61123, 65930, 68234, 70123, 67282, 65929]
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