// document.addEventListener('DOMContentLoaded', function () {
var unique_selections = {}
var filter_selections = {}

function parseDate(dateString) {
    try {
        const [datePart, timePart] = dateString.split(' ');
        const [year, month, day] = datePart.split('-');
        const [hour, minute, second] = timePart.split(':');
        return new Date(year, month - 1, day, hour, minute, second);
    } catch {
        return null

    }
}

function compareRows(a, b, columnIndex) {
    const aValue = a.children[columnIndex].textContent;
    const bValue = b.children[columnIndex].textContent;

    // Check for null values and handle them by placing them at the bottom
    if (aValue === null || aValue === '') return 1;
    if (bValue === null || bValue === '') return -1;

    const numA = parseFloat(aValue);
    const numB = parseFloat(bValue);

    // Check if both values are valid numbers
    if (!isNaN(numA) && !isNaN(numB)) {
        if (numA < numB) return -1;
        if (numA > numB) return 1;
        return 0; // numbers are equal
    }

    // Handle the case where one or both values are not valid numbers
    if (isNaN(numA) && isNaN(numB)) {
        // Both values are not valid numbers, compare as strings
        return aValue.localeCompare(bValue, undefined, { numeric: true });
    }

    // One of the values is not a valid number, treat it as greater (placed at the bottom)
    return isNaN(numA) ? 1 : -1;
}

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
            var table = document.getElementById('table');
            clearTable()
            // Create a <thead> element if it doesn't exist
            var thead = table.querySelector('thead');
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

            var all_cols = Object.keys(data[0]);
            if (initial == true) {
                var selectedCols = all_cols;
            } else {
                var selectedCols = selected_cols;
            }

            all_cols.forEach(col => {
                unique_selections[col] = [];
            })

            // Create the table header row
            const headerRow = document.createElement('tr');
            headerRow.innerHTML = '<th>#</th>';
            selectedCols.forEach(col => {
                headerRow.innerHTML += `<th id=${col}>${col}</th>`;
            });
            thead.appendChild(headerRow);

            // Loop through the data and create table rows with selected columns
            data.forEach((item, index) => {
                all_cols.forEach(col => {
                    var col_type = typeof (item[col]);
                    if (col_type != 'object') {
                        unique_selections[col].push(item[col])

                    } else {
                        unique_selections[col] = unique_selections[col].concat(item[col]);
                    }
                });
            });

            for (const key in unique_selections) {
                if (unique_selections.hasOwnProperty(key)) {
                    const valuesArray = unique_selections[key];
                    var trimmedLower = new Set();

                    valuesArray.forEach(item => {
                        if (typeof item === 'string') {
                            const trimmedLowerCaseItem = item.trim().toLowerCase();
                            trimmedLower.add(trimmedLowerCaseItem);
                        } else {
                            trimmedLower.add(item);
                        }
                    });
                    // Add the set to the new dictionary
                    unique_selections[key] = Array.from(trimmedLower);
                }
            }

            if (initial == true) {
                all_cols.forEach(col => {
                    var colArray = Array.from(unique_selections[col]);
                    var col_type = typeof (colArray[0]);
                    var select = document.getElementById('modal-content');
                    // select
                    var selectbutton = document.createElement('div');
                    selectbutton.innerHTML = '';
                    if (col_type == 'number') {
                        var maximum = Math.max(...colArray)
                        var minimum = Math.min(...colArray)
                        var cur_val_1 = minimum
                        var cur_val_2 = maximum
                        selectbutton.innerHTML +=
                            `<div class="col-selection" >
                    <label><input type="checkbox" id="${col}" checked>${col}</label>
                    <div class="slider-container">
                    <label for="minValue"> Min: </label>
                    <input type="number" id="${col}_minValue" class="range-input" value="${minimum}" step="1" min="${minimum}">
                    <br>
                    <label for="maxValue"> Max: </label>
                    <input type="number" id="${col}_maxValue" class="range-input" value="${maximum}" step="1" min="${minimum}">                            
                    <button id="exclude_null_${col}">Exclude null </button>
                    </div>
                    <p class=${col}_current-value>Current Range: from ${cur_val_1} to ${cur_val_2}</p>
                    `
                        select.appendChild(selectbutton);
                        var val_1 = document.getElementById(`${col}_minValue`);
                        var val_2 = document.getElementById(`${col}_maxValue`);
                        var currentValueLabel = document.querySelector(`.${col}_current-value`);

                        val_1.addEventListener('input', () => {
                            cur_val_1 = parseInt(val_1.value);
                            if (cur_val_1 > maximum) {
                                cur_val_1 = maximum;
                                val_1.value = maximum;
                            }
                            if (cur_val_1 > cur_val_2) {
                                cur_val_1 = cur_val_2;
                                cur_val_2 = cur_val_1;
                            }
                            filter_selections[col] = [cur_val_1, cur_val_2]
                            currentValueLabel.textContent = `Current Range: from ${cur_val_1} to ${cur_val_2}
                    `});
                        val_2.addEventListener('input', () => {
                            cur_val_2 = parseInt(val_2.value);
                            if (cur_val_2 > maximum) {
                                cur_val_2 = maximum;
                                val_2.value = maximum;
                            }
                            if (cur_val_1 > cur_val_2) {
                                cur_val_1 = cur_val_2;
                                cur_val_2 = cur_val_1;
                            }
                            filter_selections[col] = [cur_val_1, cur_val_2]
                            currentValueLabel.textContent = `Current Range: from ${cur_val_1} to ${cur_val_2}
                    `;
                        });
                        
                    filter_selections[col] = [cur_val_1, cur_val_2]
                    } else if (col == 'imdb_description') {
                        selectbutton.innerHTML += `
                    <div class="col-selection" >
                    <label><input type="checkbox" id="${col}" checked>${col}</label>
                    </div>`
                        select.appendChild(selectbutton);
                    } else if (col_type == 'string') {
                        selectbutton.innerHTML += `
                    <div class="col-selection" >
                    <label><input type="checkbox" id="${col}" checked>${col}</label>
                    <div class="dropdown-wrapper" id="${col}_dropdown-wrapper">
                    <div class="dropdown-container", id="${col}_dropdown-container">Select ${col}</div>
                    <div class="dropdown-list" id=${col}_dropdown-list></div>
                    </div>
                    <div class="col-filters">
                    <button id="exclude_null_${col}">Exclude null</button>
                    <button class="clear_selections" onClick="clearSingleSelections()">Clear selections</button>
                    <div class="selected-items" id="${col}_selected-items"></div>
                    </div>
                    `
                        select.appendChild(selectbutton);

                        var dropdownContainer = document.getElementById(`${col}_dropdown-container`);
                        var selectedItemsContainer = document.getElementById(`${col}_selected-items`);
                        var dropdownList = document.getElementById(`${col}_dropdown-list`);

                        // Populate the dropdown
                        colArray.forEach(option => {
                            var item = document.createElement("button");
                            item.className = "dropdown-item";
                            item.textContent = option;
                            item.addEventListener("click", () => selectOption(option,col));
                            dropdownList.appendChild(item);
                        });

                        // Function to open/close the dropdown
                        function toggleDropdown() {
                            var current = dropdownList.style.display;
                            if (current == "block") {
                                dropdownList.style.display = 'none'
                            } else {
                                dropdownList.style.display = 'block'
                            }
                        }

                        // Function to select an option and close the dropdown
                        function selectOption(option,col) {
                            if (!filter_selections[col].has(option)) {
                                var item = document.createElement("button");
                                item.className = "select-item";
                                item.id = `${option}_select-item`;
                                item.textContent = option;
                                selectedItemsContainer.appendChild(item);
                                filter_selections[col].add(option)

                                item.addEventListener("click", () => {
                                    selectedItemsContainer.removeChild(item);
                                    filter_selections[col].add(option)
                                });
                            }
                            //console.log(filter_selections[col])
                        }

                        // Show/hide the dropdown list when clicking the container
                        dropdownContainer.addEventListener("click", () => {
                            toggleDropdown();
                        });

                        // Close the dropdown list when clicking outside of it
                        window.addEventListener("click", (event) => {
                            if (!dropdownContainer.contains(event.target)) {
                                dropdownList.classList.remove("active");
                            }
                        });
                        filter_selections[col] =  new Set();
                    }

                })
            }

            data.forEach((item, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `<th scope="row">${index + 1}</th>`;
                //console.log(filter_selections)
                var flag = true;
                //console.log(filter_selections)
                all_cols.forEach(col => {
                    var selectedarr = Array.from(selectedCols)
                    var curr_val_elem = item[col];
                    // var col_type = typeof (unique_selections[col][0]);
                    var col_type = typeof (item[col]);
                    if (selectedarr.includes(col)) {
                        if (col_type == 'number' &&
                            (item[col] <= filter_selections[col][0] &&
                                item[col] >= filter_selections[col][1])) {
                            row.innerHTML += `<td>${item[col]}</td>`;
                        } else if (col_type == 'string' && typeof (item[col]) == 'string' && (filter_selections.hasOwnProperty(col)) &&
                            ((filter_selections[col].size == 0) ||
                                (filter_selections[col].has(item[col])))) {
                            row.innerHTML += `<td>${item[col]}</td>`;
                        }  else if (col_type == 'string'  && (item[col]!=null) && (filter_selections.hasOwnProperty(col)) &&
                            (filter_selections[col].size == 0)) {
                            let result = curr_val_elem.every(num => filter_selections[col].includes(num));
                            if (result) {
                                row.innerHTML += `<td>${item[col]}</td>`;
                            } else {
                                console.log("hehe?!")
                                flag=false
                            }
                        } else if (col == 'imdb_description') {
                            row.innerHTML += `<td>${item[col]}</td>`;
                        } else {
                            flag = false;
                        }
                    }
                });
                if (flag) {
                    console.log(col, item[col],col_type)
                    tbody.appendChild(row);
                }
            });

            // Select the table headers after they are created
            const headers = thead.getElementsByTagName('th');

            // Add click event listeners to column headers for sorting
            for (let i = 0; i < headers.length; i++) {
                headers[i].addEventListener('click', () => {
                    sortTable(table, headers, i);
                });
            }
            //console.log(filter_selections)
        })
        .catch(error => console.error('Error fetching data: ', error));
}


display([], initial = true);

function clearTable() {
    // Clear the table by removing all rows and thead
    var table = document.getElementById('table');
    var thead = table.querySelector('thead');
    var tbody = table.querySelector('tbody');

    if (thead) {
        table.removeChild(thead);
    }

    if (tbody) {
        table.removeChild(tbody);
    }
}


function showColumnSelector() {
    document.getElementById('column-selector-modal').style.display = 'block';
}

function hideColumnSelector() {
    document.getElementById('column-selector-modal').style.display = 'none';
    var selectedCols = saveSelectedColumns();
    display(selectedCols, initial = false);

    // updateColumnVisibility();
}


function saveSelectedColumns() {
    // Reset the array before saving
    var selectedColumns = [];

    // Loop through all checkboxes and save selected column names
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            const columnName = checkbox.id.replace('show', '').toLowerCase();
            selectedColumns.push(columnName);
        }
    });

    //console.log('Selected Columns:', selectedColumns);
    return selectedColumns;
}


function showColumnFilter() {
    document.getElementById('column-selector-modal').style.display = 'block';
}