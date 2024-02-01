# %%
# %%
# Import pandas for data manipulation
import pandas as pd
# Import TFIDF
from sklearn.feature_extraction.text import TfidfVectorizer
# Import cosine similarity
from sklearn.metrics.pairwise import cosine_similarity

# %% [markdown]
# ## EDA
# 
# We will be running simple recommendation system based on IMDB description similarity for NLP

# %%
import pandas as pd

IMDB_PATH="data/normalized_tables/imdb.csv"

df=pd.read_csv(IMDB_PATH)
df.head()

# %%
count=len(df)
na_count=df.isna().sum()
count

# %%
na_count

# %%
tfidf = TfidfVectorizer(analyzer='word',
                      token_pattern=r'\w{1,}',
                      ngram_range=(1, 3), 
                      stop_words = 'english')

# Filling NaNs with empty string
df['imdb_description'] = df['imdb_description'].fillna('')

# %%
# Fitting the TF-IDF on the 'overview' text
tfidf_matrix = tfidf.fit_transform(df['imdb_description'])

tfidf_matrix.shape

# %%
# Compute the Cosine Similarity
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Create a pandas series with movie titles as indices and indices as series values 
indices = pd.Series(df.index, index=df['kdrama_name']).drop_duplicates()

# %% [markdown]
# ### Testing out similarities
# 
# - we will choose random movie and find top  5 movies similar to it

# %%
chosen_movie=df.sample()
chosen_movie

# %%
title=chosen_movie["kdrama_name"]

# Get the index corresponding to movie title
index = indices[title]

# Get the cosine similarity scores 
similarity_scores = list(enumerate(similarity_matrix[index][0]))

# Sort the similarity scores in descending order
sorted_similarity_scores = sorted(similarity_scores,  key=lambda x: x[1], reverse=True)

# Top-10 most similar movie scores
top_10_movies_scores = sorted_similarity_scores[1:11]

# Get movie indices
top_10_movie_indices=[]
for i in top_10_movies_scores:
    top_10_movie_indices.append(i[0])
    
res=df[['kdrama_name', 'imdb_description']].iloc[top_10_movie_indices]
print("chosen movie: ", title)
print(res)

