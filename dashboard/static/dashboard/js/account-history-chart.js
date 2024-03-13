// Get the canvas elements
var chartElement = document.getElementById('account-history-chart');
var ctx = chartElement.getContext('2d');

// Get the account history data and parse JSON format
var accountDataString = chartElement.getAttribute('my-data');
var modifiedAccountData = accountDataString.replace(/'/g, '"');
var accountData = JSON.parse(modifiedAccountData);

// Variables for account history data and labels
var accountHistoryData;
var accountHistoryLabels;
var axisTitle;

// Function to set chart fallback data
function setDefaultData() {
  accountHistoryData = accountData.today.balances;
  accountHistoryLabels = accountData.today.times;
}

// Set default data
setDefaultData();

// Create the initial chart with default data
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: accountHistoryLabels,
    datasets: [{
      label: 'Account Value',
      backgroundColor: '#69A2E0',
      borderColor: '#437DBC',
      data: accountHistoryData,
    }]
  },
  options: {
    scales: {
      x: {
        title: {
          display: true,
          text: axisTitle
        },
        grid: {
          color: '#437dbc3b'
        },
        ticks: {
          color: '#080B0E'
        }
      },
      y: {
        grid: {
          color: '#437dbc3b'
        },
        ticks: {
          color: '#080B0E'
        }
      }
    }
  }
});

// Function to update the chart data
function updateChartData() {
  myChart.data.labels = accountHistoryLabels;
  myChart.data.datasets[0].data = accountHistoryData;
  myChart.options.scales.x.title.text = axisTitle;
  myChart.update();
}

//  Gets Date buttons and adds event listener for each
var dateButtons = document.querySelectorAll('.date-buttons');
dateButtons.forEach(function (button) {
  button.addEventListener('click', function (event) {
    
    // Get the id of the clicked element
    var buttonId = event.target.id;

    // Update the account data based on which element was clicked
    if (buttonId === 'day') {
      accountHistoryData = accountData.today.balances;
      accountHistoryLabels = accountData.today.times;
      axisTitle = 'Times Throughout Day'
    } 
    
    else if (buttonId === 'month') {
      accountHistoryData = accountData.this_month.balances;
      accountHistoryLabels = accountData.this_month.days;
      axisTitle = 'Days of the Month'
    } 
    
    else if (buttonId === 'year') {
      accountHistoryData = accountData.this_year.balances;
      accountHistoryLabels = accountData.this_year.months;
      axisTitle = 'Months in the Year'
    }

    // Update the chart data
    updateChartData();
  });
});