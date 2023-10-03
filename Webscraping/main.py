import dramalist
import imdb
import movie_wiki
import json
import re
import pandas as pd

# getting dramalist from wikipedia
wikilinks=movie_wiki.get_wikilinks()
dramas=wikilinks.keys()

##test example (it is important to keep a small list for testing because websites limit number
# of requests so limiting webscraping instances is crucial)
test=['The Greatest Marriage',"Vincenzo"]

#get mydramalist korean dramalist
dramalist=dramalist.get_dramalist(dramas)
imdb=imdb.get_imdb_ratings()

#contains 'Also Known as' section of mydramalist dramalist
other_names=dramalist[1]

#store other descriptors from mydramalist
drama_descr=dramalist[0]

#stores final list of dramas
tracker=0
with_imdb={}
for drama in drama_descr.keys():
    with_imdb[drama]=drama_descr[drama]
    with_imdb[drama]['drama_name']=drama
    for movie in imdb.keys():
        if movie.lower()==drama.lower():   
            tracker+=1   
            with_imdb[drama]['imdb_rating']=imdb[movie][0]
            with_imdb[drama]['imdb_user_count']=imdb[movie][1]
            with_imdb[drama]['imdb_description']=imdb[movie][2]
            ###(testing outputs ongo helps to test data sanity)
            #print([drama,with_imdb[drama]])

for val in with_imdb:
    #formatting entries
    with_imdb[val]["Tags"][-1]=with_imdb[val]["Tags"][-1].replace("(vote or add tags)","")

df=pd.DataFrame(with_imdb)
df = df.transpose()
###storing korean drama list into a csv file
df.to_csv("data/kdramalist.csv", encoding='utf-8', index=False,na_rep="N/A")

###evaluate accuracy
print("#############lengths: ",(tracker,len(drama_descr)))
#############lengths:  (743, 1278)

