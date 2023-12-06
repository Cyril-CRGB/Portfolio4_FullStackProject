// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // to export in excel the list of Product
    // Get the button element 
    let generateButtonExcel = document.getElementById('export-excel');
    // Add click event listener to the button
    generateButtonExcel.addEventListener('click', generateExcel);
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



