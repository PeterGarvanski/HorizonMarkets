// Get the canvas elements
var chartElement = document.getElementById('account-history-chart');
var ctx = chartElement.getContext('2d');

// Get the account history data and parse JSON format
var accountDataString = chartElement.getAttribute('my-data');
var modifiedAccountData = accountDataString.replace(/'/g, '"')
var accountData = JSON.parse(modifiedAccountData);

// Fallback account history options
const accountHistoryData = accountData.today.balances
const accountHistoryLabels = accountData.today.times

// Event listener for DOM to finnish loading
document.addEventListener("DOMContentLoaded", function () {
  
//  Gets Date buttons and adds event listener for each
var dateButtons = document.querySelectorAll('.date-buttons');
  dateButtons.forEach(function (button) {
    button.addEventListener('click', function (event) {

      // Get the id of the clicked element
      var buttonId = event.target.id;

      // Update the account data based on which element was clicked
      if (buttonId === 'day') {
        accountHistoryData = accountData.today.balances
        accountHistoryLabels = accountData.today.times
      } 
      
      else if (buttonId === 'month') {
        accountHistoryData = accountData.this_month.balances
        accountHistoryLabels = accountData.this_month.days
        console.log("Month button clicked");
      } 
      
      else if (buttonId === 'year') {
        accountHistoryData = accountData.this_year.balances
        accountHistoryLabels = accountData.this_year.months
        console.log("Year button clicked");
      }
    });
  });
});


// Add Data to the chart element
var data = {
  labels: accountHistoryLabels,
  datasets: [{
    label: 'Account Value',
    backgroundColor: '#69A2E0',
    borderColor: '#437DBC',
    data: accountHistoryData,
  }]
};

// Configure the chart element
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