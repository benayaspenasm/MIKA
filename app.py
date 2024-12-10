"""
Created on Sat Dec  7 20:44:11 2024

@authors: 
    Miguel Benayas Penas
    Skarleth Motino Flores
    --> Los Chicos de Madriz

Hackathon Generative AI 2024.

"""
import streamlit as st
from functions import *
from groq import Groq
from io import BytesIO
from PIL import Image
import requests

topn = 1  # top news to create media content
memes_location = "meme_templates.txt"  # memes repository

context_refined = ''


# Title of the app
st.title('MIKA')


# Initialize session state for dropdowns and prompt if not set already
if 'user_prompt' not in st.session_state:
    st.session_state.user_prompt = ''
if 'selected_tone' not in st.session_state:
    st.session_state.selected_tone = 'Formal'
if 'selected_format' not in st.session_state:
    st.session_state.selected_format = 'Text Post'
if 'selected_platform' not in st.session_state:
    st.session_state.selected_platform = 'LinkedIn'

# Prompt input (adjusted based on the action: creating or refining)
if 'is_refining' not in st.session_state:
    st.session_state.is_refining = False

if "show_refine_button" not in st.session_state:
    st.session_state.show_refine_button = False
    
if "show_text_area" not in st.session_state:
    st.session_state.show_text_area = False  # Controls visibility of the text area

# pront for aditinal comments here
if 'user_prompt_refine' not in st.session_state:
    st.session_state.user_prompt_refine = ''



if st.session_state.is_refining:
    # If refining, we use the previous prompt and allow the user to modify it
    prompt_placeholder = "Refine your prompt here..."
else:
    prompt_placeholder = "e.g., 'Create a LinkedIn post about AI trends today.'"


st.session_state.user_prompt = st.text_area(
    "Enter your prompt here",
    value=st.session_state.user_prompt,
    placeholder=prompt_placeholder
)

# Create columns for side-by-side layout
col1, col2, col3= st.columns(3)

# Add dropdowns to respective columns
with col1:
    # Dropdown for selecting tone
    tone_options = ['Formal', 'Humorous', 'Casual', 'Professional']
    st.session_state.selected_tone = st.selectbox(
        'Select Tone',
        tone_options,
        index=tone_options.index(st.session_state.selected_tone),
        key='tone_selectbox'
    )


with col2:
    # Dropdown for selecting content format
    format_options = ['Text Post', 'Image', 'Meme', 'Video']
    st.session_state.selected_format = st.selectbox(
        'Select Format',
        format_options,
        index=format_options.index(st.session_state.selected_format),
        key='format_selectbox'
    )

with col3:
    # Dropdown for selecting platform
    platform_options = ['LinkedIn', 'Instagram', 'X', 'Facebook',  'TikTok']
    st.session_state.selected_platform = st.selectbox(
        'Select Platform',
        platform_options,
        index=platform_options.index(st.session_state.selected_platform),
        key='platform_selectbox'
    )   


# Button to submit the request
if st.button('Generate Post'):
    if st.session_state.user_prompt:
        # Display the selected values
        st.write(f"**Prompt:** {st.session_state.user_prompt}")
        st.write(f"**Tone:** {st.session_state.selected_tone}")
        st.write(f"**Format:** {st.session_state.selected_format}")
        st.write(f"**Platform:** {st.session_state.selected_platform}")
        st.write("\nGenerating your post... Please wait.")
        
        
        # Checking whether we are dealing with a new post or just refining a previous one. 
        # If we are refining, then we add extra context provided by the context_refined variable
        try: 
            if st.session_state.user_prompt_refine != '' : 
                context_refined = f' Additionally, you shall {st.session_state.user_prompt_refine}' 
        except:
            pass 
        
        
        topic = askGroq(question="extract from the the sentence the topic he or she wants to search. Your response should be only one sentence in quote marks, do not add something like 'the topic is' as an introduction", context=f'the sentence is {st.session_state.user_prompt}')
       
       
        # Get the top news from Google News API
        today_news = get_today_news(keyword=topic, max=10, period='2d', country='United States', language='english')
        
        ## fetching only the topn articles. In this case, we are just fetching one for simplicity
        successful_retrievals = 0
        articles = []
        
        for idx in range(len(today_news)):
            article, article_url = get_full_content_a(idx=idx, json_news_list=today_news)
                        
            try:
                article['error'] = None
            except:
                articles.append(article)
                successful_retrievals += 1
            
            if successful_retrievals == topn:
                break
            
            
        # printing the source url 
        st.markdown(f'Source URL: {article_url}' )
        
        
        ## if - else for the different types of posts
        if st.session_state.selected_format == format_options[0]: # generating text post
            text_post = askGroq(question=f"create a {st.session_state.selected_platform} post summarizing this following article : {article}", context=f'You are an article summarizer who uses a {st.session_state.selected_tone} tone. Ensure the post is under 300 characters and includes relevant emojis. {context_refined}')
            st.markdown(text_post)
            
        elif st.session_state.selected_format == format_options[1]: # generating image
            
            Image =  get_image(topic, st.session_state.selected_tone)
            st.image(Image, caption="AI Generated Image", use_container_width=True)
            
            
            # Convert the image back to bytes for downloading
            img_buffer = BytesIO()
            Image.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            
            # Provide a download button
            st.download_button(
                label="Download Image",
                data=img_buffer,
                file_name="generated_image.png",
                mime="image/png"
                )
            # Placeholder for Image-related logic
            
        elif st.session_state.selected_format == format_options[2]:# generating meme
            list_of_templates = read_templates_file(memes_location)

            input_string = askGroq(question=f"Given the list of meme templates below, which meme would you use to be added to the following article: {article}. List of templates: {list_of_templates}. Give your answer saying only the ID and Text_suggested in the format: ID: 00000000. Text1:'text' and Text2:'text'. Do not describe the meme.", context= context_refined)
            template_id, text1, text2 = extract_details(input_string)


            url_meme = create_imgflip_meme("melissa2024", "Telehonduritas2024", str(template_id), text1, text2)
            
            st.image(url_meme[1], use_container_width=True)
            
            # Allow users to download the meme
            imagebytes = requests.get(url_meme[1]).content  # Get the image content from the URL
            st.download_button(
                label="Download meme", 
                data=imagebytes,  # Image data in bytes
                file_name="meme.jpeg",  # File name for download
                mime="image/jpeg"  # MIME type
            )

        else:
            video_transcript = askGroq(question=f"create a {st.session_state.selected_platform} post summarizing this following article : {article}", context=f'You are an article summarizer who uses a {st.session_state.selected_tone} tone. Ensure the post is under 280 characters and do not include emojis. { context_refined}')
            
            video_url = get_video(video_transcript)
                        
            st.video(video_url)
            
            # Allow users to download the video
            imagebytes = requests.get(video_url).content  # Get the video content from the URL
            st.download_button(
                label="Download video", 
                data=imagebytes,  # Video data in bytes
                file_name="video.mp4",  # File name for download
                mime="video/mp4"  # MIME type
            )
            
    
        # Show textarea
        st.session_state.show_text_area = True
    
    
    else:
        st.warning("Please enter a prompt to generate the post.")

    
    st.session_state.show_refine_button = True

# Button to toggle the visibility of the text area

if st.session_state.show_refine_button:
    
        
            
    # Conditionally display the text area
    if st.session_state.show_text_area:
        st.session_state.user_prompt_refine = st.text_area(
            "You may enter additional comments to refine your post",
            value=st.session_state.user_prompt_refine,
            placeholder="Additional context for your prompt here..."  
            
        )

        
if st.button("Reset"):
    # Reset specific session state variables
    st.session_state.show_refine_button = False  # Keep this True if you want the refine button to appear again
    st.session_state.show_text_area = False
    st.session_state.user_prompt_refine = ""  # Reset the user input for refinement
    st.session_state.user_prompt = ''

    st.success("Session state has been reset.")   
            


# Display session state for debugging purposes (optional)
# st.write("Session State:", st.session_state)
