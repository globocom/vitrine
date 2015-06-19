var commits2Stackbars, plotCommitsChart;

commits2Stackbars = function(data) {
  var chartData, item, month, proj, projects, year;
  projects = {};
  for (year in data) {
    for (month in data[year]) {
      item = year + '/' + month;
      for (proj in data[year][month]) {
        if (!projects[proj]) {
          projects[proj] = [];
        }
        projects[proj].push([item, data[year][month][proj]]);
      }
    }
  }
  chartData = Object.keys(projects).map(function(key) {
    return projects[key];
  });
  return chartData;
};

plotCommitsChart = function(placeholder, data) {
  $.plot(placeholder, commits2Stackbars(data), {
    series: {
      stack: 0,
      bars: {
        fill: 1.0,
        show: true,
        barWidth: 0.6,
        lineWidth: 0
      }
    },
    colors: ['#4A8DE5', '#F7A807', '#B6EB83', '#D25461'],
    xaxis: {
      mode: 'categories',
      tickLength: 0
    },
    grid: {
      borderWidth: 0,
      aboveData: true,
      markings: [
        {
          color: '#E5E5E5',
          lineWidth: 1,
          xaxis: {
            from: 4,
            to: 4
          }
        }, {
          color: '#E5E5E5',
          lineWidth: 1,
          xaxis: {
            from: 8,
            to: 8
          }
        }
      ]
    }
  });
};
