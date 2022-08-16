import csv
import re

sett=set()
with open('../kdramalist.csv',newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for i in csv_reader:
        part=i[7]
        sett.add(part)

    for i in sett:
        print(i)











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





        