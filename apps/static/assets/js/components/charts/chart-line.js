'use strict';

var SalesChart = (function () {

  var canvas = document.getElementById('chart-sales-dark');
  var dataEl = document.getElementById('eventos-data');

  if (!canvas || !dataEl) return;

  var labels = JSON.parse(dataEl.dataset.labels);
  var datos  = JSON.parse(dataEl.dataset.datos);

  new Chart(canvas, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Eventos por mes',
        data: datos,
        tension: 0.4,
        fill: true,
        backgroundColor: 'rgba(78,115,223,0.1)',
        borderColor: 'rgba(78,115,223,1)',
        borderWidth: 2,
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

})();
