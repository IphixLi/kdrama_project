import csv
import re
import json


data={}
with open('data/kdramalist.csv',newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    j=1
    for i in csv_reader:
            values={}
            values['drama_name']=i[17]
            #genres
            genres_part=i[0].split(",")
            genres_part=[re.sub('[^A-Za-z ]','',g) for g in genres_part]
            values['genre']=genres_part

            #tags
            tags=i[1].split(",")
            tags=[re.sub('[^A-Za-z ]','',t) for t in tags]
            values['tags']=tags

            values['episodes']=i[3]

            #start airing
            if "," in i[4]:
                start_airing='-'.join([i[4][5:7],i[4][1:4],i[4][len(i[4])-2:len(i[4])]])
            else:
                start_airing=i[4]
            values['start_airing']=start_airing

            values['end_airing']=i[5]

            #airedon
            airedon=i[6].split(",")
            airedon=[re.sub('[^A-Za-z ]','',a) for a in airedon]
            values['aired_on']=airedon

            #network
            networks_part=i[7].split(",")
            networks_part=[re.sub('[^A-Za-z ]','',g) for g in networks_part]
            values['original_network']=networks_part


            values['duration']=i[8]
            values['score']=i[9]
            values['scored_by']=i[10]
            values['ranked']=i[11]
            values['popularity']=i[12]
            values['content_rating']=i[13]
            values['watchers']=i[14]
            #actors
            actors=i[15].split(",")
            actors=[re.sub('[^A-Za-z ]','',a) for a in actors]
            values['actors']=actors

            #platforms
            platforms=i[16].split(",")
            platforms=[re.sub('[^A-Za-z ]','',a) for a in platforms]
            values['platforms']=platforms

            values['imdb_rating']=i[18]
            values['imdb_users']=i[19]
            values['imdb_description']=i[20]
            data[str(j)]=values
            j+=1
    print(len(data))
    csv_file.close() 
jsonfile = open("data/jsonfile.json", "w")
json.dump(data, jsonfile, indent = 6)  
jsonfile.close()
