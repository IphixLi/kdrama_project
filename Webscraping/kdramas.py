from bs4 import BeautifulSoup
import requests

def get_wikilinks():
    url="https://en.wikipedia.org/wiki/List_of_South_Korean_dramas"
    r=requests.get(url)
    soup=BeautifulSoup(r.content,"html.parser",from_encoding='utf-8')

    x=soup.find_all('ul')
    start=0
    movies={}
    for i in x:
        if start>=2:
            break
        for a in i.find_all('a', href=True):
            if a['href']=="#See_also":
                start+=1
            elif a['href']=="/wiki/List_of_South_Korean_television_series":
                start+=1
                break
            elif start:
                movies[a.get_text().strip()]="https://en.wikipedia.org"+a['href']
    return movies


if __name__=="__main__":
    a=get_wikilinks()
    for i in a.items():
        print(i)

