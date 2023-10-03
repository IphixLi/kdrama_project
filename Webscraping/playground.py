import csv
import re
import pandas as pd

dramalist=set()
with open('./kdramalist.csv',newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for i in csv_reader:
        if 
        dramalist.append(i)



"""
def get_imdb_ratings():
    ratings={}
    ids={}
    id=1
    url="https://www.imdb.com/search/title/?title_type=tv_series&countries=kr"
    while '/search/title/?title_type=tv_series&countries=kr' in url:
        r=requests.get(url+"&view=simple").content
        soup=BeautifulSoup(r,"html.parser",from_encoding="utf-8")

        x=soup.findAll(class_='lister-item-content')
        for i in x:
            movie_link=i.find('a')['href']
            link=requests.get(movie_link+"?ref_=adv_li_tt").content
            soup=BeautifulSoup(link,"html.parser",from_encoding="utf-8")


if __name__=="__main__":
    get_imdb_ratings()
    #for i in sorted(u[1].keys()):
    #  print(i)
"""





        async function get_data() {
    try {
        const response = await fetch('../data/jsonfile.json');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

async function display() {
    try {
        const tableBody = document.getElementById("table");
        const data = await get_data(); // Wait for data to be fetched
        console.log(data);
        const items = Object.keys(data);
        console.log(items);

        // Create table header
        const headerRow = document.createElement('tr');
        items.forEach(item => {
            const th = document.createElement('th');
            th.textContent = item;
            headerRow.appendChild(th);
        });
        tableBody.appendChild(headerRow);

        // Loop through the data and create table rows
        for (const row_val of Object.values(data)) {
            const row = document.createElement('tr');
            items.forEach(item => {
                const td = document.createElement('td');
                td.textContent = row_val[item];
                row.appendChild(td);
            });
            tableBody.appendChild(row);
        }
    } catch (error) {
        console.error('Error displaying data:', error);
    }
}

// Call the display function
display();
