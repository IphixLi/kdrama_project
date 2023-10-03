function parseDate(dateString) {
    try{
        const [datePart, timePart] = dateString.split(' ');
        const [year, month, day] = datePart.split('-');
        const [hour, minute, second] = timePart.split(':');
        return new Date(year, month - 1, day, hour, minute, second);
    } catch {
        return null
        
    }
    }



// Function to compare rows based on column values
function compareRows(a, b, columnIndex) {
    const aValue = a.children[columnIndex].textContent;
    const bValue = b.children[columnIndex].textContent;

    // Handle null values by placing them at the bottom
    if (aValue === null || aValue === '') return 1;
    if (bValue === null || bValue === '') return -1;

    // Parse the date strings into Date objects
    const dateA = parseDate(aValue);
    const dateB = parseDate(bValue);

    // Check if the parsing was successful
    if (!isNaN(dateA) && !isNaN(dateB)) {
        // Compare the parsed dates
        if (dateA < dateB) return -1;
        if (dateA > dateB) return 1;
        return 0; // Dates are equal
    }

    // If parsing fails or values are not valid dates, compare them as strings
    return aValue.localeCompare(bValue, undefined, { numeric: true });
}

    // Function to sort the table rows
    function sortTable(table, headers, columnIndex) {
        // Toggle sorting direction (asc or desc)
        const currentDirection = headers[columnIndex].getAttribute('data-direction');
        const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';

        // Update data-direction attribute for all headers
        for (let i = 0; i < headers.length; i++) {
            headers[i].removeAttribute('data-direction');
        }
        headers[columnIndex].setAttribute('data-direction', newDirection);

        // Select the tbody element
        const tbody = table.querySelector('tbody');

        // Select the table rows from the tbody
        const rows = Array.from(tbody.querySelectorAll('tr'));

        // Sort the rows
        rows.sort((a, b) => {
            return compareRows(a, b, columnIndex) * (newDirection === 'asc' ? 1 : -1);
        });

        // Clear the tbody
        tbody.innerHTML = '';

        // Append the sorted rows back to the tbody
        rows.forEach(row => {
            tbody.appendChild(row);
        });
    }

    function display(selected_cols, initial = true) {
        // Fetch data from the server
        fetch('../data/jsonfile.json')
            .then(response => response.json())
            .then(data => {
                // Get the table element
                const table = document.getElementById('table');

                // Create a <thead> element if it doesn't exist
                const thead = table.querySelector('thead');
                if (!thead) {
                    thead = document.createElement('thead');
                    table.appendChild(thead);
                }

                // Create a <tbody> element if it doesn't exist
                let tbody = table.querySelector('tbody');
                if (!tbody) {
                    tbody = document.createElement('tbody');
                    table.appendChild(tbody);
                }

                // Define the selected columns
                if (initial == true) {
                    var selectedCols = Object.keys(data[0]);
                } else {
                    var selectedCols = selected_cols;
                }

                // Create the table header row
                const headerRow = document.createElement('tr');
                headerRow.innerHTML = '<th>#</th>';
                selectedCols.forEach(col => {
                    headerRow.innerHTML += `<th id=${col}>${col}</th>`;
                });
                thead.appendChild(headerRow);

                // Loop through the data and create table rows with selected columns
                data.forEach((item, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<th scope="row">${index + 1}</th>`;
                    selectedCols.forEach(col => {
                        row.innerHTML += `<td>${item[col]}</td>`;
                    });
                    tbody.appendChild(row);
                });

                // Select the table headers after they are created
                const headers = thead.getElementsByTagName('th');

                // Add click event listeners to column headers for sorting
                for (let i = 0; i < headers.length; i++) {
                    headers[i].addEventListener('click', () => {
                        sortTable(table, headers, i);
                    });
                }
            })
            .catch(error => console.error('Error fetching data: ', error));
    }

    const selectedCols = [
        "kdrama_name", "actors", "tags", "episodes", "start_airing", "end_airing", "duration",
        "score", "scored_by", "ranked", "popularity", "content_rating"
    ];

    display(selectedCols, initial = true);

