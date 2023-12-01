// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // to export in excel the list of Product
    // Get the button element 
    let generateButtonExcel = document.getElementById('export-excel');
    // Add click event listener to the button
    generateButtonExcel.addEventListener('click', generateExcel);

    //CHARTJS
    // Fetch the chart data from the Django view
    fetch("{% url 'chart_data' %}")
        .then(response => response.json())
        .then(chartData => {
            // Extract data for Chart.js, unique years
            const uniqueYears = [...newnew Set(chartData.map(item => item.gd_year))];

            // Prepare datasets for Chart.js based on unique years
            const datasets = uniqueYears.map(year => {
                const dataByYear = chartData.filter(item => item.gd_year === year);
                const data = dataByYear.map(item => parseFloat(item.gd_paid_salary));
                return {
                    label: `Year ${year}`,
                    data: data,
                    borderColor: getRandomColor(), // Implement getRandomColor function
                    fill: false,
                };
            });

            // Extract unique months from chartData
            const uniqueMonths = [...new Set(chartData.map(item => item.gd_month))];

            // Render the chart
            var ctx = document.getElementById('myChart').getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: uniqueMonths,
                    datasets: datasets,    
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
        })
        .catch(error => console.error('Error fetching chart data:', error));
});


/**
 * This function will allow the user to export the new table in excel
 */
function generateExcel() {
    //Create a new workbook
    let workbook = XLSX.utils.book_new();

    //Get the new table by its ID
    let excelTable = document.getElementById("data-table");

    // Check if the table is empty
    if (excelTable.children[1].innerHTML === '' || excelTable.rows.length === 0) {
        alert("The table is empty!");
        return;
    }

    //Create a worksheet
    let worksheet = XLSX.utils.aoa_to_sheet([]);

    // Loop through each row of excelTable and add data to the worksheet
    for (let i = 0; i < excelTable.rows.length; i++) {
        let rowData = [];
        let cells = excelTable.rows[i].cells;

        // Loop through each cell of the row and add its value to rowData
        for (let j = 0; j < cells.length; j++) {
            rowData.push(cells[j].textContent);
        }

        // Add the row data to the worksheet
        XLSX.utils.sheet_add_aoa(worksheet, [rowData], { origin: -1 });
    }

    // Add the worksheet to the workbook
    XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");

    // Save the workbook as an Excel file
    XLSX.writeFile(workbook, "output.xlsx");
}


/**
 * Function to generate a random color for chart datasets
 */
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}