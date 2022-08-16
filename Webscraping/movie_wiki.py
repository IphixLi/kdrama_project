from bs4 import BeautifulSoup
import requests
from kdramas import get_wikilinks

wikilinks=get_wikilinks()
dramas=wikilinks.keys()
links=wikilinks.values()

##for getting actors (not effective as some wikipages have completely different html make-up)
def get_movielist(dramalist):
    main_characters={}
    for url in dramalist:
            r=requests.get(url.rstrip()).content
            soup=BeautifulSoup(r,"html.parser")
            actors=[]
            for field in soup.select('li',title=True):
                if field.find_previous('h3') and 'main' not in field.find_previous('h3').text.lower():
                    continue
                else:
                    if ' as ' in field.get_text():
                        actors.append(field.get_text().split(' as ')[0])
            main_characters[url.split('wiki/')[-1]]=actors[:8]
    return main_characters

if __name__=="__main__":
    print(get_movielist(links))


        