// JavaScript code to load and visualize data using Highcharts

// Load the CSV file using AJAX or fetch
// Replace 'your_data.csv' with the actual path or filename of your CSV file
fetch("static/visdata/10101_rcp26_annual_tm_ensemble.csv")
    .then(response => response.text())
    .then(data => {
        const rows = data.trim().split('\n');
        const headers = rows[6].split(',');
        const years = [];
        const values = [];

        const medianColumnIndex = headers.indexOf("Median");

        for (let i = 7; i < rows.length; i++) {
            const row = rows[i].split(',');
            years.push(parseInt(row[0]));
            values.push(parseFloat(row[medianColumnIndex]));
        }

        console.log(years);
        console.log(values);

        const series = [{
          type: 'line',
          name: 'Median',
          data: values
      }];

        Highcharts.chart('chartContainer', {
            title: {
                text: 'Climate Change Data Visualization (Median)'
            },
            xAxis: [{
                ordinal:false,
                categories: years,
                title: {
                  text: "Time"
                }
            }],
            yAxis: {
                title: {
                    text: 'Mean temperature [°C]'
                }
            },
            series: series
        });
    });
