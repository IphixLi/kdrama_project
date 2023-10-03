const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose(); // Import SQLite
const app = express();
const port = 3000;
const path = require('path');
const cors = require('cors');

// Enable CORS for all routes (or specify origins)
app.use(cors());

// Specify the absolute path to the SQLite database file
const dbPath = path.join(__dirname, '', 'kdrama_database.db');
console.log(dbPath)
// Middleware to parse JSON requests
app.use(bodyParser.json());

// Create a SQLite database connection
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Error opening database:', err);
    } else {
        console.log('Database opened successfully');
    }
});

app.get('/', (req, res) => {
    console.error('api for retrieving kdramas');
    res.status(200).json({data:"success"})
        })

// API endpoint to get all dramas
app.get('/dramas', (req, res) => {
    db.all('SELECT *,GROUP_CONCAT(a.actor) as actors FROM main_descriptors \
        join actors a on a.kdrama_name = main_descriptors.kdrama_name \
         GROUP BY main_descriptors.kdrama_name; ', (err, rows) => {
            if (err) {
                console.error('Error fetching data:', err);
                res.status(500).json({ error: 'Error fetching data' });
            } else {
                res.status(200).json(rows);
            }
        });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
