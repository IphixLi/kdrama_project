// document.addEventListener('DOMContentLoaded', function () {
var unique_selections = {}
var filter_selections = {}
const DESCR = {
    "kdrama_name": " Name of a Korean Drama",
    "genre":"Genre of a Korean Drama",
    "tags": "Tags associated with a Korean drama",
    "episodes": "episodes in Korean drama",
    "start_airing": "The year the Korean drama started to be shown in",
    "end_airing": "The year the Korean drama ended to be shown in",
    "aired_on": "The day the Korean drama was first aired on",
    "original_network": "The platform the Korean drama was first aired on",
    "duration": "How long the Korean drama lasts",
    "scored_by": "How many people scored the korean drama on kdramalist website",
    "ranked": "How the korean drama on kdramalist website was scored",
    "popularity": "",
    "content_rating": "",
    "watchers": "",
    "actors": "",
    "platforms": "",
    "imdb_rating": "",
    "imdb_users": "",
    "imdb_description":""
}

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

                        var no_colArray=colArray.filter(value => typeof value === 'number' && !isNaN(value));
                        var minimum = Math.min(...no_colArray)
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
                            filter_selections[col] = [col_type, [cur_val_1, cur_val_2]]
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
                            filter_selections[col] = [col_type, [cur_val_1, cur_val_2]]
                            currentValueLabel.textContent = `Current Range: from ${cur_val_1} to ${cur_val_2}
                        `;
                        });

                        filter_selections[col] = [col_type, [cur_val_1, cur_val_2]]
                    } else if (col =='kdrama_name' || col == 'imdb_description') {
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
                        <button class="clear_selections" id="${col}_clearSingleSelections">Clear selections</button>
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
                            item.addEventListener("click", () => selectOption(option, col));
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


                        var clear_selections = document.getElementById(`${col}_clearSingleSelections`)
    
                        clear_selections.addEventListener('click', () => {
                            console.log(selectedItemsContainer)
                            filter_selections[col][1] = new Set();
                            var childDivs = selectedItemsContainer.querySelectorAll("button");

                            // Loop through and remove each child div
                            childDivs.forEach(function(child) {
                                selectedItemsContainer.removeChild(child);
                            });
                        })

                        // Function to select an option and close the dropdown
                        function selectOption(option, col) {
                            if (!filter_selections[col][1].has(option)) {
                                var item = document.createElement("button");
                                item.className = "select-item";
                                item.id = `${option}_select-item`;
                                item.textContent = option;
                                selectedItemsContainer.appendChild(item);
                                filter_selections[col][1].add(option)
                                console.log(selectedItemsContainer)
                                
                                item.addEventListener("click", () => {
                                    selectedItemsContainer.removeChild(item);
                                    filter_selections[col][1].delete(option)
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
                        filter_selections[col] = [col_type, new Set()];
                    }

                })
            }

            var filteredData = data;

            // Apply filters
            if (initial==false) {
                filteredData = filterData(data, filter_selections);
            }
            
            filteredData.forEach((item, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `<th scope="row">${index + 1}</th>`;
                all_cols.forEach(col => {
                    var selectedarr = Array.from(selectedCols)
                    if (selectedarr.includes(col)) {
                        row.innerHTML += `<td>${item[col]}</td>`;
                        tbody.appendChild(row);
                    }
                })
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


function showColumnSelector(event) {
    event.stopPropagation();
    document.getElementById('column-selector-modal').style.display = 'block';
}

function hideColumnSelector() {
    document.getElementById('column-selector-modal').style.display = 'none';
    var selectedCols = saveSelectedColumns();
    display(selectedCols, initial = false);

    // updateColumnVisibility();
}

document.getElementById('modal-content').addEventListener('click', function(event) {
    event.stopPropagation();
});

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




// data_sample=[      {
//     "kdrama_name": "100 Days My Prince",
//     "genre": [
//           "historical",
//           " comedy",
//           " romance",
//           " drama"
//     ],
//     "tags": [
//           "amnesia",
//           " hidden identity",
//           " marriage of convenience",
//           " joseon dynasty",
//           " fake marriage",
//           " eccentric male lead",
//           " hardworking female lead",
//           " double identity",
//           " strong female lead",
//           " riches to rags "
//     ],
//     "episodes": 16,
//     "start_airing": "2018-09-10 00:00:00",
//     "end_airing": "2018-10-30 00:00:00",
//     "aired_on": [
//           "tuesday",
//           " monday"
//     ],
//     "original_network": [
//           "tvN"
//     ],
//     "duration": 75,
//     "scored_by": 26483,
//     "ranked": 906,
//     "popularity": 140,
//     "content_rating": "15+ - Teens 15 or older",
//     "watchers": 56458,
//     "actors": [
//           "Doh Kyung Soo",
//           " Nam Ji Hyun",
//           " Kim Seon Ho",
//           " Han So Hee",
//           " Jo Sung Ha",
//           " Kim Jae Young"
//     ],
//     "platforms": [
//           "iQIYI",
//           " Viki",
//           " WeTV",
//           " Netflix",
//           " Apple TV"
//     ],
//     "imdb_rating": 7.8,
//     "imdb_users": 3309,
//     "imdb_description": "Upon losing his memory, a crown prince encounters a commoner's life and experiences unforgettable love as the husband to Joseon's oldest bachelorette."
// },
// {
//     "kdrama_name": "12 Signs of Love",
//     "genre": [
//           "comedy",
//           " romance",
//           " life"
//     ],
//     "tags": [
//           "writer female lead "
//     ],
//     "episodes": 16,
//     "start_airing": "2012-02-15 00:00:00",
//     "end_airing": "2012-04-05 00:00:00",
//     "aired_on": [
//           "wednesday",
//           " thursday"
//     ],
//     "original_network": [
//           "tvN"
//     ],
//     "duration": 65,
//     "scored_by": 907,
//     "ranked": 8243,
//     "popularity": 4110,
//     "content_rating": "Not Yet Rated",
//     "watchers": 2588,
//     "actors": [
//           "Ohn Joo Wan",
//           " Yoon Jin Seo",
//           " Lee Yong Woo",
//           " Bae Geu Rin",
//           " Go Joon Hee",
//           " Kim Sung  Je"
//     ],
//     "platforms": [
//           ""
//     ],
//     "imdb_rating": null,
//     "imdb_users": null,
//     "imdb_description": "N/A"
//     },]

// selection_sample={"platforms":["string",Set("Viki","tvN")],"actors":["string",Set(["Yoon Jin Seo","Bae Geu Rin")], "duration":["number",[30,68]]}
 
// Filters
function filterData(data, selections) {
    //console.log(data, selections)
    return data.filter((entry) => {
        for (const column in selections) {
            const [type, values] = selections[column];
            if (type === "string") {
                // value of a given column from data row
                const entryValue = entry[column];
                //console.log("now", entryValue, values, column)
                if (values.size== 0 || hasValueInSet(entryValue, values)) {
                    //console.log("wait what")
                    continue; // Move on to the next filter
                } else {
                    return false; // Filter out this entry
                }
            } else if (type === "number") {
                const entryValue = entry[column];
                const [minval, maxval] = values;
                if (entryValue >= minval && entryValue <= maxval) {
                    continue; // Move on to the next filter
                } else {
                    //console.log("now", entryValue, values, column)
                    return false; // Filter out this entry
                }
            }
        }
        return true; // Include the entry if it passes all filters
    });
}


function hasValueInSet(valueList, mySet) {
    if (Array.isArray(valueList)) {
        for (var value of valueList) {
            var temp = value.trim().toLowerCase();
            if (mySet.has(temp)) {
                return true;
            }
        }
    } else {
        if (mySet.has(valueList.trim().toLowerCase())) {
            return true;
        }
    }
    return false;
}


