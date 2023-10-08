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
app.get('/alldramas', (req, res) => {
    var command = `SELECT
    main_descriptors.kdrama_name,
    GROUP_CONCAT(genres.genre) AS genre,
    GROUP_CONCAT(tags.tags) AS tags,
    main_descriptors.episodes,
    CAST(main_descriptors.start_airing as DATETIME) as start_airing,
    CAST(main_descriptors.end_airing as DATETIME) as end_airing,
    GROUP_CONCAT(aired.day) AS aired_on,
    GROUP_CONCAT(original_networks.original_networks) AS original_network,
    main_descriptors.duration,
    main_descriptors.scored_by,
    main_descriptors.ranked,
    main_descriptors.popularity,
    main_descriptors.content_rating,
    main_descriptors.watchers,
    GROUP_CONCAT(actors.actor) AS actors,
    GROUP_CONCAT(platforms.platform) AS platforms,
    imdb.imdb_rating,
    imdb.imdb_users,
    imdb.imdb_description
FROM main_descriptors
LEFT JOIN (
    SELECT kdrama_name, imdb_rating, imdb_users, imdb_description
    FROM imdb
) AS imdb ON imdb.kdrama_name = main_descriptors.kdrama_name
LEFT JOIN (
    SELECT kdrama_name, GROUP_CONCAT(genre) AS genre
    FROM genres
    GROUP BY kdrama_name
) AS genres ON genres.kdrama_name = main_descriptors.kdrama_name
LEFT JOIN (
    SELECT kdrama_name, GROUP_CONCAT(tags) AS tags
    FROM tags
    GROUP BY kdrama_name
) AS tags ON tags.kdrama_name = main_descriptors.kdrama_name
LEFT JOIN (
    SELECT kdrama_name, GROUP_CONCAT(day) AS day
    FROM aired
    GROUP BY kdrama_name
) AS aired ON aired.kdrama_name = main_descriptors.kdrama_name
LEFT JOIN (
    SELECT kdrama_name, GROUP_CONCAT(original_networks) AS original_networks
    FROM original_networks
    GROUP BY kdrama_name
) AS original_networks ON original_networks.kdrama_name = main_descriptors.kdrama_name
LEFT JOIN (
    SELECT kdrama_name, GROUP_CONCAT(actor) AS actor
    FROM actors
    GROUP BY kdrama_name
) AS actors ON actors.kdrama_name = main_descriptors.kdrama_name
LEFT JOIN (
    SELECT kdrama_name, GROUP_CONCAT(platform) AS platform
    FROM platforms
    GROUP BY kdrama_name
) AS platforms ON platforms.kdrama_name = main_descriptors.kdrama_name
GROUP BY main_descriptors.kdrama_name
limit 4;
;`
    
    
    db.all(command, (err, rows) => {
        if (err) {
            console.error('Error fetching data:', err);
            res.status(500).json({ error: 'Error fetching data' });
        } else {
            console.log(rows)
            res.status(200).json(rows)
        };
    });
})

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
