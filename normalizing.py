import csv,re
import pandas as pd


main_descriptors_table=[]
imdb_table=[]
platforms_table=[]
aired_table=[]
actors_table=[]
genres_table=[]
tags_table=[]
networks_table=[]


with open('Webscraping/kdramalist.csv',newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for i in csv_reader:

        #genres
        genres_part=i[1].split(",")
        genres_part=[re.sub('[^A-Za-z ]','',g) for g in genres_part]
        namegen=[[i[0],j] for j in genres_part]
        genres_table+=namegen

        #networks
        networks_part=i[7].split(",")
        networks_part=[re.sub('[^A-Za-z ]','',g) for g in networks_part]
        net=[[i[0],j] for j in networks_part]
        networks_table+=net
        
        #tags
        tags=i[2].split(",")
        tags=[re.sub('[^A-Za-z ]','',t) for t in tags]
        ngtags=[[i[0],j] for j in tags]
        tags_table+=ngtags

        #aired on
        airedon=i[6].split(",")
        airedon=[re.sub('[^A-Za-z ]','',a) for a in airedon]
        waired=[[i[0],j] for j in airedon]
        aired_table+=waired

        #actors
        actors=i[15].split(",")
        actors=[re.sub('[^A-Za-z ]','',a) for a in actors]
        wactors=[[i[0],j] for j in actors]
        actors_table+=wactors

        #platforms
        platforms=i[16].split(",")
        platforms=[re.sub('[^A-Za-z ]','',a) for a in platforms]
        wplatforms=[[i[0],j] for j in platforms]
        platforms_table+=wplatforms
        
        #main_descriptors

        #format start airing date for easy transformation
        if "," in i[4]:
            start_airing='-'.join([i[4][5:7],i[4][1:4],i[4][len(i[4])-2:len(i[4])]])
        else:
            start_airing=i[4]
        #removing redudancy attributes country and favorites
        descr=[i[0],i[3],start_airing,i[5],i[8],i[9],i[10],i[11],i[12],i[13],i[14]]
        main_descriptors_table.append(descr)

        #imdb
        if i[17]!='N/A' or i[18]!='N/A' or i[19]!='N/A':
            imdb_rating=re.findall("\d+\.?\d*",i[17])
            if len(imdb_rating)!=0:
                imdb_part=[i[0],imdb_rating[0],i[18],i[19]]
            else:
                imdb_part=[i[0],i[17],i[18],i[19]]
            imdb_table.append(imdb_part)
        
    #defining headers for each table
    cols_main=['Kdrama_name','Episodes','start airing','end airing', 'Duration', 'score', 'scored by','Ranked',
         'Popularity', 'Content Rating','Watchers']
    cols_imdb=['kdrama_name','imdb_rating','imdb_users','imdb_description']
    cols_aired=['kdrama_name','day']
    cols_platforms=['kdrama_name','platform']
    cols_actors=['kdrama_name','actor']
    cols_genre=['kdrama_name','genre']
    cols_tags=['kdrama_name','tags']
    cols_networks=['kdrama_name','original_networks']

    #save to csv files

    #main descriptors
    df_main = pd.DataFrame(main_descriptors_table[1:], columns=cols_main)
    df_main.to_csv("data/normalized_tables/main_descriptors.csv", encoding='utf-8', index=False)

    #imdb
    df_imdb = pd.DataFrame(imdb_table[1:], columns=cols_imdb)
    df_imdb.to_csv("data/normalized_tables/imdb.csv", encoding='utf-8', index=False)

    #original_networks
    df_networks = pd.DataFrame(networks_table[1:], columns=cols_networks)
    df_networks.to_csv("data/normalized_tables/networks.csv", encoding='utf-8', index=False)
    #aired
    df_aired = pd.DataFrame(aired_table[1:], columns=cols_aired)
    df_aired.to_csv("data/normalized_tables/aired_on.csv", encoding='utf-8', index=False)

    #platforms
    df_plat = pd.DataFrame(platforms_table[1:], columns=cols_platforms)
    df_plat.to_csv("data/normalized_tables/platforms.csv", encoding='utf-8', index=False)

    #actors
    df_actors = pd.DataFrame(actors_table[1:], columns=cols_actors)
    df_actors.to_csv("data/normalized_tables/actors.csv", index=False)

    #genres
    df_genres = pd.DataFrame(genres_table[1:], columns=cols_genre)
    df_genres.to_csv("data/normalized_tables/genres.csv", encoding='utf-8', index=False)

    #tags
    df_tags = pd.DataFrame(tags_table[1:], columns=cols_tags)
    df_tags.to_csv("data/normalized_tables/tags.csv", encoding='utf-8', index=False)
        