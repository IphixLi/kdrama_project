from dramalist import get_dramalist
from imdb import get_imdb_ratings
from kdramas import get_wikilinks
import json
import re
import pandas as pd

# getting dramalist from wikipedia
wikilinks=get_wikilinks()
dramas=wikilinks.keys()

##test example (it is important to keep a small list for testing because websites limit number
# of requests so limiting webscraping instances is crucial)
test=['The Greatest Marriage',"Vincenzo"]

#get mydramalist korean dramalist
dramalist=get_dramalist(dramas)
imdb=get_imdb_ratings()

#contains 'Also Known as' section of mydramalist dramalist
other_names=dramalist[1]

#store other descriptors from mydramalist
drama_descr=dramalist[0]

#stores final list of dramas
with_imdb={}
for movie in imdb.keys():
    for drama in drama_descr.keys():
        #check if drama name from imdb is same as name in mydramalist name or is in
        # 'Also known as' section of mydramalist descriptors
        if drama in other_names.keys() and (movie.lower()==drama.lower() or (movie.lower() in other_names[drama])):
            with_imdb[drama]=drama_descr[drama]
            with_imdb[drama]['imdb_name']=movie
            with_imdb[drama]['imdb_rating']=imdb[movie][0]
            with_imdb[drama]['imdb_user_count']=imdb[movie][1]
            with_imdb[drama]['imdb_description']=imdb[movie][2]
            ###(testing outputs ongo helps to test data sanity)
            #print([drama,with_imdb[drama]])
for val in with_imdb:
    #formatting entries
    with_imdb[val]["Tags"][-1]=with_imdb[val]["Tags"][-1].replace("(vote or add tags)","")
    temp=re.findall("\d+\.?\d*",with_imdb[drama]["imdb_rating"])
    if len(temp)==1:
        with_imdb[drama]["imdb_rating"]=temp[0]

df=pd.DataFrame(with_imdb)
df = df.transpose()
###storing korean drama list into a pandas dataframe
df.to_csv("kdramalist.csv", encoding='utf-8', index=False,na_rep="N/A")

###evaluate accuracy
print("#############lengths: ",(len(with_imdb),len(drama_descr)))
#############lengths:  (743, 1278)

