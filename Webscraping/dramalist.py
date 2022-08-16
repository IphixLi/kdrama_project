from bs4 import BeautifulSoup
import re
import requests
from kdramas import get_wikilinks

#obtain korean dramalist from wikipedia
wikilinks=get_wikilinks()
dramas=wikilinks.keys()
links=wikilinks.values()



def get_dramalist(dramalist):
    dramas={}
    other_names={}
    #initial search URI
    slug="https://mydramalist.com/search?q="


    #look for link of each the kdrama in its html make-up
    for movie in dramalist:
            formatted="+".join(re.sub('[^A-Za-z0-9\s\.]', '', movie.rstrip()).lower().split(" "))
            r=requests.get(slug+formatted)
            soup=BeautifulSoup(r.content.decode('utf-8', 'ignore'),"html.parser")
            x=soup.findAll('div',id=True)
            link=""
            for div in x:
                temp=div['id'].split("-")[-1].strip()
                if temp.isnumeric()==True and 'mdl' in div['id'] and len(temp)>=4 and link=="":
                    span=div.find('span',class_='text-muted').get_text()
                    if 'Korean Drama' in span:
                        links=div.find('a',href=True)
                        link=links['href']
                        break
            
            #identified URL of drama
            url="https://mydramalist.com"+link
            m=requests.get(url)
            soup=BeautifulSoup(m.content.decode('utf-8', 'ignore'),"html.parser")

            m=soup.find(class_='show-detailsxss')
            descr={}
            if m==None:
                continue
            else:
                x=m.findAll('li')
                for i in x:
                    temp=i.get_text().split(":")
                    if len(temp)!=2:
                        continue
                    else:   ##get drama descriptors
                            if temp[0].strip()=='Country' and temp[1].strip()=='South Korea':
                                descr[temp[0]]=temp[1].strip()
                            elif temp[0].strip()=='Country' and temp[1].strip()!='South Korea':
                                continue
                            elif temp[0].strip() in ['Episodes','Content Rating','Watchers','actors']:
                                descr[temp[0]]=temp[1].strip()
                            elif temp[0].strip()=='Also Known As':
                                other_names[movie]=[i.strip().lower() for i in temp[1].split(", ")]
                            elif temp[0].strip()=='Original Network':
                                names=i.findAll('a')
                                networks=[]
                                for j in names:
                                    networks.append(j.get_text().strip())
                                descr[temp[0]]=networks
                            elif temp[0].strip()=='Aired':
                                split=temp[1].split(" -")
                                if len(split)==2:
                                    descr['start airing']=split[0].strip()
                                    descr['end airing']=split[1].strip()
                                else:
                                    descr['start airing']=split[0]

                            elif temp[0].strip() in ['Genres','Tags','Aired On']:
                                descr[temp[0]]=[i.strip().lower() for i in temp[1].split(", ")]
                            elif temp[0].strip() in ['Ranked','Popularity']:
                                split=temp[1].strip()
                                descr[temp[0]]=split[1:]
                            elif temp[0].strip()=='Score':
                                split=temp[1].split(" by")
                                score=''.join(re.findall("\d+\.?\d*",split[0]))
                                users=''.join(re.findall("\d+\.?\d*",split[1]))
                                if len(score)>0 and len(users)>0 and len(split)==2:
                                    descr['score']=score
                                    descr['scored by']=users
                            elif temp[0].strip()=='Duration':
                                split=temp[1].split("hr")
                                hr=''.join(filter(str.isdigit, split[0]))
                                minute=''.join(filter(str.isdigit, split[-1]))
                                if len(hr)>0 and len(minute)>0 and len(split)==2:
                                    descr['Duration']=int(hr)*60+int(minute)
                                elif  len(split)==1 and len(minute)>0:
                                    descr['Duration']=int(minute)
                                #print([movie,other_names[movie]])



            m=soup.find(class_='p-a-sm')
            if m!=None:
                actors=m.findAll('b')
                actor_list=[]
                for actor in actors:
                    actor_list.append(actor.get_text())
                descr['actors']=actor_list

            #get_platforms
            m=soup.findAll('div',class_='p-l')
            platforms=[]
            for i in m:
                x=i.find('b')
                if len(x)>0:
                    platforms.append(x.get_text().strip())
            descr['platforms']=platforms
          
            if len(descr)>0 and 'Country' in descr.keys() :
                dramas[movie]=descr
                #print(dramas[movie])
    return (dramas,other_names)

if __name__=="__main__":
    
    test=['Live On','The Greatest Marriage',"It's Okay to Not Be Okay"]
    a=get_dramalist(test)[0].items()






