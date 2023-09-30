import csv
import re
import json
import pprint

data={}
with open('kdramalist.csv',newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for i in csv_reader:
        values={}
        #genres
        genres_part=i[1].split(",")
        genres_part=[re.sub('[^A-Za-z ]','',g) for g in genres_part]
        values['genre']=genres_part

        #networks
        networks_part=i[7].split(",")
        networks_part=[re.sub('[^A-Za-z ]','',g) for g in networks_part]
        values['original_network']=list(networks_part)
        
        #tags
        tags=i[2].split(",")
        tags=[re.sub('[^A-Za-z ]','',t) for t in tags]
        values['tags']=tags

        #aired on
        airedon=i[6].split(",")
        airedon=[re.sub('[^A-Za-z ]','',a) for a in airedon]
        values['aired_on']=airedon


        #actors
        actors=i[15].split(",")
        actors=[re.sub('[^A-Za-z ]','',a) for a in actors]
        values['actors']=actors


        #platforms
        platforms=i[16].split(",")
        platforms=[re.sub('[^A-Za-z ]','',a) for a in platforms]
        values['platforms']=platforms

        #format start airing date for easy transformation
        if "," in i[4]:
            start_airing='-'.join([i[4][5:7],i[4][1:4],i[4][len(i[4])-2:len(i[4])]])
        else:
            start_airing=i[4]
        values['episodes']=i[3]
        values['start_airing']=start_airing
        values['end_airing']=i[5]
        values['original_network']=i[7]
        values['duration']=i[8]
        values['score']=i[9]
        values['scored_by']=i[10]
        values['ranked']=i[11]
        values['popularity']=i[12]
        values['content_rating']=i[13]
        values['watchers']=i[14]
        values['imdb_rating']=i[17]
        values['imdb_users']=i[18]
        values['imdb_description']=i[19]
        data[i[0]]=values

    csv_file.close() 
out_file = open("myfile.json", "w")
json.dump(data, out_file, indent = 6)  
out_file.close()
