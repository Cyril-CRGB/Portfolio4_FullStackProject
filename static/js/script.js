// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Use jsPDF and TableExport to export to PDF
    document.getElementById('export-pdf').addEventListener('click', function () {
        var pdf = new jsPDF('p', 'pt', 'letter');
        pdf.autoTable({ html: '#data-table' });
        pdf.save('data.pdf');
    });

    // Use TableExport to export to Excel
    document.getElementById('export-excel').addEventListener('click', function () {
        TableExport(document.getElementById('data-table'), {
            formats: ['js-xlsx'],
            exportButtons: false
        }).export();
    });
});