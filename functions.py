#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 20:56:46 2024

@author: admin
"""

import re # standard library
import os # standard library
from groq import Groq
import requests
from gnews import GNews
from googlenewsdecoder import new_decoderv1
import base64
from io import BytesIO
from PIL import Image
from time import sleep


# Get the top n news from Google of the US in the last 24h
def get_today_news( keyword = 'technology', max = 3, period = '1d', country = 'United States', language = 'english'  ):
      # Initialize GNews
      google_news = GNews()

      # Hyperparameters
      google_news.period = period  # News from last 7 days
      google_news.max_results = max  # number of responses across a keyword
      google_news.country = country # News from a specific country
      google_news.language = language  # News in a specific language
      google_news.exclude_websites = ['reuters.com','msn.com']


      # Get news for a specific topic
      today_news  = google_news.get_news(keyword)


      # Print today's news
      for news in today_news:
          print(f"Title: {news['title']}")
          print(f"Published Date: {news['published date']}")
          print(f"Link: {news['url']}\n")

      return today_news;


def get_imgflip_templates():
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            memes = data["data"]["memes"]
            return memes
        else:
            print("Error:", data["error_message"])
            return []
    else:
        print(f"HTTP Error: {response.status_code}")
        return []



def read_templates_file(file_path):
    try:
        # Open the file in read mode
        with open(file_path, "r") as file:
            # Read the entire content of the file
            list_of_templates = file.read()
        return list_of_templates
    except FileNotFoundError:
        return "The file does not exist. Please make sure the file path is correct."
    
    


# Function to create meme
#

def create_imgflip_meme(username, password, template_id, text0, text1):
    url = "https://api.imgflip.com/caption_image"
    payload = {
        "template_id": template_id,
        "username": username,
        "password": password,
        "text0": text0,
        "text1": text1
    }
    response = requests.post(url, data=payload)
    if response.json()["success"]:
        print("Meme URL:", response.json()["data"]["url"])
        return ("Meme URL:", response.json()["data"]["url"])
    else:
        print("Error:", response.json()["error_message"])
        
        

# Function to extract the id, and texts from the response 

def extract_details(input_string):
    try:
        # Extract the ID using regex
        id_match = re.search(r"ID:\s*(\d+)", input_string)
        template_id = id_match.group(1) if id_match else None

        # Extract Text1 inside the first pair of single quotes
        text1_match = re.search(r"Text1:\s*'(.*?)'", input_string)
        text1 = text1_match.group(1) if text1_match else None

        # Extract Text2 inside the second pair of single quotes
        text2_match = re.search(r"Text2:\s*'(.*?)'", input_string)
        text2 = text2_match.group(1) if text2_match else None

        return template_id, text1, text2
    except Exception as e:
        return f"Error: {e}"
    
    
    
def askGroq(question = "just say hello world", context = ''):
    

    groq_key = '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'

    client = Groq(
        # This is the default and can be omitted
        api_key=groq_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content





def get_full_content_a(idx=0, json_news_list=None):
    """
    Retrieve the full content of an article from a list of news articles.

    Parameters:
        idx (int): Index of the article in the list.
        json_news_list (list): List of news articles in JSON format.

    Returns:
        dict: Full content of the article or an error message if unavailable.
    """
    
    # Initialize GNews
    google_news = GNews()
    
    # Validate input
    if not json_news_list or idx < 0 or idx >= len(json_news_list):
        return {"error": "Invalid index or empty news list"}

    try:
        
        interval_time = 1 # this can change to any time, but 5 is recommended
        decoded_url = new_decoderv1(json_news_list[idx]['url'], interval=interval_time)
        
        # Fetch the article using the URL
        article = google_news.get_full_article(decoded_url['decoded_url'])
        return article.text, decoded_url['decoded_url']
    except Exception as e:
        # Handle any errors during fetching
        return {"error": str(e)}


def get_image(topic, tone):
    
    stabilityai_key = 'sk-Died6F4skmUDQuY3wINyD9c4ZSvX1jcOPEIpK0XaQZ9RwedO'

    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={
            "authorization": f"Bearer {stabilityai_key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": f"{topic} with a {tone} tone",
            "output_format": "webp",
        },
    )

    # Convert byte data to an image
    image = Image.open(BytesIO(response.content))
    
    
    return image


def get_video(transcript):
    
    heygen_key = 'ZWI0NjhjZDYzNDkyNDE0MGI5OWUyM2ZmMzI1YzlmZGEtMTczMzU5Njk5NA=='

    url = "https://api.heygen.com/v2/video/generate"

    headers = {  
        "accept": "application/json",  
        "content-type": "application/json",  
        "x-api-key": heygen_key,  
    }

    # Define the payload (data to be sent in the request)
    data = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": "Brent_sitting_office_front",  # Avatar ID
                    "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": transcript,  # Input text for the voice
                    "voice_id": "ff2ecc8fbdef4273a28bed7b5e35bb57", # Voice ID
                    "speed" : 0.8
                }
            }
        ],
        "caption": False,
        "dimension": {
            "width": 150,
            "height": 150
        }
    }

    res = requests.post(url, headers=headers, json=data)

    #print(res.json())


    #time.sleep()



    url = "https://api.heygen.com/v1/video_status.get"

    headers = {"accept": "application/json", "x-api-key": heygen_key }

    params = {
        "video_id": res.json()['data']['video_id']  # Replace with the actual video ID
    }

    
    sleep(120)
    
    response = requests.get(url, headers=headers,  params=params)
    
    
    return response.json()['data']['video_url']
    
    
    