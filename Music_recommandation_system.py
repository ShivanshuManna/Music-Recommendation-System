# Import necessary libraries
import pandas as pd  # For data handling and manipulation
import joblib  # For loading saved models or data
import streamlit as st  # For creating the web app interface
import requests  # For making HTTP requests to fetch image data
from PIL import Image  # For handling and displaying images
from io import BytesIO  # For handling image data
import datetime  # For formatting date information

# Read music data from an Excel file
data = pd.read_excel('Music_Data.xlsx')

# Load pre-computed similarity matrix and TF-IDF vectorizer
similarity_matrix = joblib.load('similarity_matrix.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Set the title of the web app
st.title('Music Recommendation App')

# Create a text input field for user to enter a song name with a default value
user_input_song = st.text_input('Enter a song name:', 'Buried Alive Interlude').lower()

# Define a function to recommend similar songs
def recommend_songs(user_input_song):
    user_input_song = user_input_song.lower()
    # Find the index of the user's input song in the dataset
    song_index = data[data['Name'].str.lower() == user_input_song].index[0]
    # Calculate the similarity of this song with others
    similar_songs = list(enumerate(similarity_matrix[song_index]))
    # Sort the songs by similarity and take the top 5 (excluding the input song itself)
    sorted_similar_songs = sorted(similar_songs, key=lambda x: x[1], reverse=True)[1:6]
    recommended_song_indices = [x[0] for x in sorted_similar_songs]
    recommended_songs = data.loc[recommended_song_indices]
    return recommended_songs

# If the "Recommend Songs" button is clicked, perform recommendation
if st.button('Recommend Songs'):
    recommended_songs = recommend_songs(user_input_song)

    # Display recommended songs and their details
    for index, row in recommended_songs.iterrows():
        # Fetch and display the song's image
        img_data = requests.get(row['Image Url']).content
        img = Image.open(BytesIO(img_data))
        st.image(img, caption=row['Name'], use_column_width=True)

        # Display song details
        st.text(f"Name: {row['Name']} \t\t\t\t\t Release Date: {(row['Release Date']).strftime('%d-%b-%y')}")
        st.text(f"Album Name: {row['Album Name']} \t\t Popularity: {row['Popularity']}")
        st.text(f"Artist Name: {row['Artist Name']}")
        st.text(f"Genre/Tags: {row['Tags']}")
        st.text(f"Speechiness: {row['Speechiness']} \t\t\t\t Acousticness: {row['Acousticness']}")
        st.text(f"Danceability: {row['Danceability']} \t\t\t\t Liveness: {row['Liveness']}")
        st.text(f"Energy: {row['Energy']} \t\t Loudness: {row['Loudness']} \t Tempo: {row['Tempo']}")
        st.text(f"Mode: {row['Mode']} \t\t Key: {row['Key']} \t\t Instrumentalness: {row['Instrumentalness']}")
        st.text(f"Valence: {row['Valence']} \t\t\t\t\t Time Signature: {row['Time Signature']}")
        
        # Generate a Spotify link for the song and make it a clickable link
        spotify = f'<a href="https://open.spotify.com/track/{row["ID"]}" style="text-decoration: none; color: inherit;" target="_blank">Spotify</a>'
        st.markdown(spotify, unsafe_allow_html=True)
        st.text('\n\n')  # Add some space between recommendations

# Create a sidebar for additional features
st.sidebar.title('Discover the music')

# Allow the user to select a song from a dropdown menu
selected_song = st.sidebar.selectbox('Select a song:', data['Name'])

# If a song is selected, display its details and a link to Spotify
if selected_song:
    song_details = data[data['Name'] == selected_song]
    st.sidebar.subheader(song_details['Name'].values[0])
    st.sidebar.text(f"Artist: {song_details['Artist Name'].values[0]}")
    st.sidebar.text(f"Album: {song_details['Album Name'].values[0]}")
    spotify = f'<a href="https://open.spotify.com/track/{song_details["ID"].values[0]}" style="text-decoration: none; color: inherit;" target="_blank">Want to listen to this track now??</a>'
    st.sidebar.markdown(spotify, unsafe_allow_html=True)

# Display an "About" section to provide information about the app
st.markdown('### About')
st.markdown("This is a simple music recommendation app based on text-based similarity.")
