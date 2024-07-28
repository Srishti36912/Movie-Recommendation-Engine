# streamlit run movie_recomm.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#loading data
@st.cache_data
def load_data():
    df = pd.read_csv('imdb_top_1000.csv')
    df = df.dropna()
    print(df.shape)
    df = df.sort_values('IMDB_Rating', ascending=False)

    def clean_gross_value(value):
        if isinstance(value, str):
            return float(value.replace(",",''))
        return 0
    df.Gross = df.Gross.apply(clean_gross_value)
    return df



# configure the layout
st.set_page_config(
    layout="wide",
    page_title="FilmCity",
    page_icon="🎥",
)

# loading data
with st.spinner("Loading Data..."):
    df = load_data()
    st.sidebar.success("Home")
    

    st.title('FilmCity 🎬')
    st.markdown(":red[Welcome to Your Ultimate Movie Recommendation Hub!] ")
    st.subheader("Discover movies you'll love based on your unique tastes and preferences. Find new favorites by exploring personalized recommendations just for you. Browse through curated lists, trending films, and hidden gems. Create your watchlist and never miss a movie again. Experience the joy of discovering new movies tailored to your interests.")
    st.header('MOVIES FROM ALL OVER THE WORLD 🍿')
    st.image('https://vfs.edu/sites/all/themes/vfs/img/programs/alumni/2022-VFS-Alumni-Success-Desktop.jpg',)

    st.title('Choose from a wide variety of movies 🎦')
    c1 ,c2 = st.columns(2)
    movies = df.Series_Title.unique().tolist()
    genre = df.Genre.unique().tolist()
    c1.metric('Total Movies ', len(movies))
    c2.metric('Total Genre' , len(genre))
    st.header("Top 10 Movies 🏆")

    c1, c2 = st.columns(2)
    top_10 = df.head(10)['Series_Title']
    c1.dataframe(top_10, use_container_width=True)
    fig_10 = px.bar(df.head(10), 'Series_Title', 'No_of_Votes')
    c2.plotly_chart(fig_10, use_container_width=True)

    st.header('Highest Rated Movies with Their Gross Profit 👑')
    scatter = px.scatter(df, 'IMDB_Rating','No_of_Votes', size='Gross', hover_name='Series_Title')
    st.plotly_chart(scatter, use_container_width=True)

    c1, c2 = st.columns(2)
    c1.header('Gross Profit with Increasing Years 💲')
    fig_area = px.area(df,'Released_Year','Gross')
    c1.plotly_chart(fig_area, use_container_width=True)
    c2.header('Certification 📜')
    fig_pie = px.funnel_area(df, 'Certificate', 'No_of_Votes')
    c2.plotly_chart(fig_pie, use_container_width=True)

    st.header('Select Genre 🎭')
    c1, c2 = st.columns(2)
    
    sel_genre = c1.selectbox('Genre',genre)

    total = df[df['Genre'] == sel_genre]
    c2.metric('Total movies: ', len(total))
    posters = df[df['Genre'] == sel_genre]['Poster_Link'].unique().tolist()
    series = df[df['Genre'] == sel_genre]['Series_Title'].unique().tolist()
    rate = df[df['Genre'] == sel_genre]['IMDB_Rating'].unique().tolist()
    votes = df[df['Genre'] == sel_genre]['No_of_Votes'].unique().tolist()
    c1.table(series)
    c2.image(posters)

    st.header('Select the Movie 📼')
    sel_movie = st.selectbox('Choose the movie',series)

    c1, c2 = st.columns([1,2])
    pos = df[df['Series_Title'] == sel_movie].head(1)['Poster_Link'].values[0]
    c1.image(pos, width=300)
    year = df[df['Series_Title'] == sel_movie].head(1)['Released_Year'].values[0]
    rating = df[df['Series_Title'] == sel_movie].head(1)['IMDB_Rating'].values[0]
    time = df[df['Series_Title'] == sel_movie].head(1)['Runtime'].values[0]
    director = df[df['Series_Title'] == sel_movie].head(1)['Director'].values[0]
    star1 = df[df['Series_Title'] == sel_movie].head(1)['Star1'].values[0]
    star2 = df[df['Series_Title'] == sel_movie].head(1)['Star2'].values[0]
    star3 = df[df['Series_Title'] == sel_movie].head(1)['Star3'].values[0]
    star4 = df[df['Series_Title'] == sel_movie].head(1)['Star4'].values[0]
    oview = df[df['Series_Title'] == sel_movie].head(1)['Overview'].values[0]
    c2.header('Movie Details: ')
    c2.metric('Released year: ', year)
    c2.metric('IMDb Rating: ', rating)
    c2.metric('Runtime: ', time)
    c2.metric('Director: ', director)
    c2.metric("Stars: ", f"{star1} , {star2} , {star3}, {star4}")
    st.header('Overview: ')
    st.subheader(oview)
