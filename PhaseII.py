import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from data_mappings import MY_FAVES, MUSIC_BLURB, GAME_HOURS, CHESS_DATA, STEAM_IMG, STEAM_URL

def toppage():
    st.title("My Interests")
    st.write("This page shares some of my personal hobbies and interests because I couldn't think of anything more creative.")

def interests():
    if 'compatibility_score' not in st.session_state:
        st.session_state.compatibility_score = 0 #new

    st.header("Games")
    st.write("I love playing video games of all kinds. Click below to see how many hours I have in one of my favorites.")

    try_favorite = st.radio("Select a game.", list(GAME_HOURS.keys())) #new
    hours = GAME_HOURS[try_favorite]

    fig, ax = plt.subplots()
    ax.barh(try_favorite, hours, color='limegreen')
    ax.set_xlabel("Hours Played")
    ax.set_xlim(0, 1000)
    st.pyplot(fig)

    st.markdown(
        f'<a href="{STEAM_URL}" target="_blank">'
        f'<img src="{STEAM_IMG}" width="100"/></a>',
        unsafe_allow_html=True
    )

    st.header("Music")
    st.write(MUSIC_BLURB)

    if st.toggle("Click to see a song I recommend to everybody I know"): #new
        st.write("Pot Kettle Black by Wilco")

    st.write("Move the sliders to show how much you like each genre, and see how compatible you are with me based on my favorites!")

    st.header("Your Genre Preferences")
    user_scores = {}
    for genre in MY_FAVES:
        key = f"genre_{genre}"
        if key not in st.session_state:
            st.session_state[key] = 5
        st.session_state[key] = st.slider(f"How much do you like {genre}?", 0, 10, st.session_state[key])
        user_scores[genre] = st.session_state[key]

    st.header("Compatibility results")
    total_difference = sum(abs(MY_FAVES[genre] - user_scores[genre]) for genre in MY_FAVES)
    max_difference = len(MY_FAVES) * 10
    raw_score = total_difference / max_difference
    st.session_state.compatibility = 100 - int(raw_score * 100)

    st.metric("Compatibility score", f"{st.session_state.compatibility}%")
    st.progress(st.session_state.compatibility / 100)

    st.header("Taste Comparison Charts")
    genres = list(MY_FAVES.keys())
    my_ratings = list(MY_FAVES.values())
    user_ratings = [user_scores[genre] for genre in genres]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    ax1.bar(genres, my_ratings, color='skyblue')
    ax1.set_title("My Ratings")
    ax1.set_ylim(0, 10)
    ax1.set_ylabel("Score")

    ax2.bar(genres, user_ratings, color='salmon')
    ax2.set_title("Your Ratings")
    ax2.set_ylim(0, 10)

    st.pyplot(fig)

    st.header("Chess")
    st.write("I started actually getting into chess in 2021, and although I don't play as much anymore, it'll forever be one of my favorite things to do.")

    df = pd.DataFrame(CHESS_DATA)
    df['date'] = pd.to_datetime(df['date'])

    fig, ax = plt.subplots()
    ax.plot(df['date'], df['rating'], marker='o')
    ax.set_title('Chess Progress Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Rating')
    ax.grid(True)

    st.pyplot(fig)

toppage()
interests()

