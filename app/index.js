function test() {
    const fs = require('fs');
    let rawdata = fs.readFileSync('jsonfile.json');
    let posts = JSON.parse(rawdata);
    for ( var [key, value] of Object.entries(posts)){
        console.log(key)
    }
};

var categories=["name","genre", "tags", "episodes", "start_airing", "end_airing", "aired_on",
    "original_network", "duration","score","scored_by","ranked","popularity",
    "content_rating", "watchers", "actors", "platforms", "imdb_rating", "imdb_users",
    "imdb_description"]

function createtags(categories, tagSelector) {
    let tagsholder = document.querySelector(tagSelector);
    if (tagsholder) {
            html = `
            <th class="category">${categories[0]}</th>
            <th class="category">${categories[1]}</th>
            <th class="category">${categories[2]}</th>
            <th class="category">${categories[3]}</th>
            <th class="category">${categories[4]}</th>
            <th class="category">${categories[5]}</th>
            <th class="category">${categories[6]}</th>
            <th class="category">${categories[7]}</th>
            <th class="category">${categories[8]}</th>
            <th class="category">${categories[9]}</th>
            <th class="category">${categories[10]}</th>
            <th class="category">${categories[11]}</th>
            <th class="category">${categories[12]}</th>
            <th class="category">${categories[13]}</th>
            <th class="category">${categories[14]}</th>
            <th class="category">${categories[15]}</th>
            <th class="category">${categories[16]}</th>
            <th class="category">${categories[17]}</th>
            <th class="category">${categories[18]}</th>
            <th class="category">${categories[19]}</th>
        `
    let container = document.createElement("tr");
    container.className = "header";
    container.innerHTML = html;
    tagsholder.append(container);
    }
}

function alldrama(data,tagSelector) {
    let holder = document.querySelector(tagSelector);
    for (var [key, value] of Object.entries(data)) {
        key_html = `
        <td class="category">${key}</td>
        <td class="category">${value.genre}</td>
        <td class="category">${value.tags}</td>
        <td class="category">${value.episodes}</td>
        <td class="category">${value.start_airing}</td>
        <td class="category">${value.end_airing}</td>
        <td class="category">${value.aired_on}</td>
        <td class="category">${value.original_network}</td>
        <td class="category">${value.duration}</td>
        <td class="category">${value.score}</td>
        <td class="category">${value.scored_by}</td>
        <td class="category">${value.ranked}</td>
        <td class="category">${value.popularity}</td>
        <td class="category">${value.content_rating}</td>
        <td class="category">${value.watchers}</td>
        <td class="category">${value.actors}</td>
        <td class="category">${value.platforms}</td>
        <td class="category">${value.imdb_rating}</td>
        <td class="category">${value.imdb_users}</td>
        <td class="category">${value.imdb_description}</td>`
        let keycontainer = document.createElement("tr");
        keycontainer.className = "tags";
        keycontainer.innerHTML = key_html;
        holder.append(keycontainer);
        }
}
   



