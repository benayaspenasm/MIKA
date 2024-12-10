#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 20:44:11 2024

@author: admin
"""


import requests
from functions import *

# Example usage
templates = get_imgflip_templates()

 

# Open a file in write mode
with open("meme_templates.txt", "w") as file:
    # Loop through the templates and write each to the file
    for meme in templates:
        file.write(f"ID: {meme['id']}, Name: {meme['name']}, URL: {meme['url']}\n")

print("Meme templates saved to 'meme_templates.txt'")




# Call the function and store the content in the variable
file_path = "meme_templates.txt"  # Specify the path to the file
list_of_templates = read_templates_file(file_path)

# Print the string variable to verify the content
print(list_of_templates)
