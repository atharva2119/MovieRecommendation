# -*- coding: utf-8 -*-
"""MovieRecommendation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10yqlW5hiteeLZ747BObgDlMr2dhDI6eq

## **Movie Recommendation System**
Recommender System is a system that seeks to predict or filter preferences according to the user's choices. Recommender systems are utilized in a variety of areas including movies, music, news, books, research articles, search queries, social tags, and products in general. Recommender systems produce a list of recommendations in any of the two ways-

Collaborative filtering: Collaborative filtering approaches build a model from the user's past behavior (i.e. items purchased or searched by the user) as well as similar decisions made by other users. This model is then used to predict items (or ratings for items) that users may have an interest in

Content-based filtering: Content-based filtering approaches uses a series of discrete characteristics of an item in order to recommend additional items with similar properties. Content-based filtering methods are totally based on a description of the item and a profile of the user's preferences. It recommends items based on the user's past preferences. Let's develop a basic recommendation system using Python and Pandas

Let's develop a basic recommendation system by suggesting items that are most similar to a particular item, in this case, movies. It just tells what movies/items are most similar to the user's movie choice.

# **Import Library**
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
import streamlit as st

# Load dataset
df = pd.read_csv('https://raw.githubusercontent.com/YBIFoundation/Dataset/main/Movies%20Recommendation.csv')

# Streamlit app title
st.title("Movie Recommendation System")

# Display dataset information
if st.checkbox('Show Dataset Info'):
    st.dataframe(df)

# Feature selection
df_features = df[['Movie_Genre', 'Movie_Keywords', 'Movie_Tagline', 'Movie_Cast', 'Movie_Director']].fillna('')
x = df_features['Movie_Genre'] + ' ' + df_features['Movie_Keywords'] + ' ' + df_features['Movie_Tagline'] + ' ' + df_features['Movie_Cast'] + ' ' + df_features['Movie_Director']

# Convert text to tokens
tfidf = TfidfVectorizer()
x = tfidf.fit_transform(x)

# Calculate similarity score
similarity_score = cosine_similarity(x)

# User input for favorite movie
favourite_movie_name = st.text_input('Enter your favorite movie name:')

if favourite_movie_name:
    All_movies_title_list = df['Movie_Title'].tolist()
    Movie_Recommendation = difflib.get_close_matches(favourite_movie_name, All_movies_title_list)
    
    if Movie_Recommendation:
        Close_Match = Movie_Recommendation[0]
        Index_of_Close_Match_Movie = df[df.Movie_Title == Close_Match]['Movie_ID'].values[0]
        
        # Getting list of similar movies
        Recommendation_Score = list(enumerate(similarity_score[Index_of_Close_Match_Movie]))
        
        # Sorting movies based on similarity score
        Sorted_Similar_Movies = sorted(Recommendation_Score, key=lambda x: x[1], reverse=True)
        
        # Display recommendations
        st.write("Top 10 movies suggested for you:")
        for i, movie in enumerate(Sorted_Similar_Movies[1:11]):  # Exclude the first one as it's the input movie
            index = movie[0]
            title_from_index = df[df.index == index]['Movie_Title'].values[0]
            st.write(f"{i+1}. {title_from_index}")
    else:
        st.write("No close match found for the given movie name.")
