import streamlit as st # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv() #loads all the environment variables
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyCIdEZJK6cu1KsmPHLQGgAAV_H3guA24sQ"


import google.generativeai as genai # type: ignore

from youtube_transcript_api import YouTubeTranscriptApi # type: ignore

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

prompt = """You are Youtube Video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 250 words . The summary will be displayed here :  """

# This is the Transcript text from YT videos 
def extract_transcript_details(youtube_video_url):
    try:
        video_id =youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " "
        for i in transcript_text:
            transcript += i['text'] + " "

        return transcript

    except Exception as e:
        raise e

# This is getting the summary of the video based on the prompt from Google Gemini Pro 
def generate_gemini_content(transcript_text, promt):

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(promt+transcript_text)
    return response.text

st.title('Youtube Video Summarizer')
youtube_link = st.text_input('Enter youtube video link : ')

if youtube_link:
    video_id =youtube_link.split("=")[1]
    st.image(f'http://img.youtube.com/vi/{video_id}/0.jpg', use_column_width=True)

if st.button('Get Detailed Notes'):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.header('Transcript:')
        st.write(summary)
        