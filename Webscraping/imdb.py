from bs4 import BeautifulSoup
import re
import requests

def get_imdb_ratings():
    ratings={}
    ids={}
    url="https://www.imdb.com/search/title/?title_type=tv_series&countries=kr"
    while '/search/title/?title_type=tv_series&countries=kr' in url:
        r=requests.get(url)
        soup=BeautifulSoup(r.content.decode('utf-8', 'ignore'),"html.parser")

        x=soup.findAll(class_='lister-item-content')
        for i in x:
            movie_link=i.find('a')['href']
            title=i.find('a',href=True,title=False).get_text()
            if i.find(class_='rating-list')==None:
                continue
            elif len(i.find(class_='rating-list')['title'].split("("))==2:
                rating=i.find(class_='rating-list')['title'].split("(")[0].split("/")[0][-3:].strip()
                temp=re.findall("\d+\.?\d*",rating.strip())
                if len(temp)==1:
                    rating=temp[0]
                votes=i.find(class_='rating-list')['title'].split("(")[1].split(")")[0][:-6]
                description=""
                link=requests.get("https://www.imdb.com"+movie_link+"plotsummary?ref_=tt_ov_pl")
                moviesoup=BeautifulSoup(link.content.decode('utf-8', 'ignore'),"html.parser")
                u=moviesoup.find('li',class_='ipl-zebra-list__item')
                if u!=None:
                    if "It looks like we don't have any Plot Summaries for this title yet" in u.get_text().strip():
                        description='N/A'
                    else:
                        description=u.get_text().strip()
                ratings[title.strip()]=(rating,votes,description)
                print((title.strip(),description))
                #print(description)
                
        next_page=soup.find(class_='lister-page-next')
        if next_page==None:
            break
        url="https://www.imdb.com"+next_page['href']
    return ratings



if __name__=="__main__":
    u=get_imdb_ratings()
    for i in u.keys():
     print(i)
