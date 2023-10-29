import pickle
import streamlit as st
import pandas as pd
import requests
import base64
import zipfile

#Name of the archieve file
zip_archive = 'similarity.zip'

with zipfile.ZipFile(zip_archive, 'r') as zipf:
    # Extract the model file
    with zipf.open('similarity.pkl') as f:
        # Load the model from the extracted file
        similarity = pickle.load(f)
        
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('recommen.png')

movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movie=pd.DataFrame(movie_dict)
#similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    data=requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=28953f9f8e1af380611b54d0427c1d95")
    final=data.json()
    return "https://image.tmdb.org/t/p/w185/" + final['poster_path']

def recommend(obj):  
    recommendation=[]  
    recommend_poster=[]
    movie_indx=movie[movie['title']==obj].index[0] 
    sort_list=sorted(list(enumerate(similarity[movie_indx])),reverse=True,key=lambda x:x[1])[0:6]
    for i in sort_list:
        recommendation.append(movie.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie.iloc[i[0]].id))
    return recommendation,recommend_poster

st.title(':white[Movie Recommendation]')

movie_selected = st.selectbox(
    'Enter the movie',
    (movie['title'].values),
    )

if st.button('Recommend'):
    name,poster=recommend(movie_selected)
    
    col1, col2, col3 , col4, col5 ,col6= st.columns(spec=6,gap="large")

    with col1:
       st.write(f':white[{name[0]}]')
       st.image(poster[0],width=180)
       st.caption(':star::star::star::star:')
       st.write(f':white[{name[1]}]')
       st.image(poster[1],width=180)
       st.caption(':star::star::star:')
        
    #with col2:
    #   st.write(f':white[{name[1]}]')
    #   st.image(poster[1],width=120)
    #   st.caption(':star::star::star:')

    with col3:
       st.write(f':white[{name[2]}]')
       st.image(poster[2],width=180)
       st.caption(':star::star::star:')
       st.write(f':white[{name[3]}]')
       st.image(poster[3],width=180)
       st.caption(':star::star::star::star:')
    
    #with col4:
    #  st.write(f':white[{name[3]}]')
    #   st.image(poster[3],width=120)
    #   st.caption(':star::star::star::star:')

    with col5:
       st.write(f':white[{name[4]}]')
       st.image(poster[4],width=180)
       st.caption(':star::star::star:')
       st.write(f':white[{name[5]}]')
       st.image(poster[5],width=180)
       st.caption(':star::star::star::star:') 
    
    #with col6:
    #   st.write(f':white[{name[5]}]')
    #   st.image(poster[5],width=120)
    #   st.caption(':star::star::star::star:')
    
    
