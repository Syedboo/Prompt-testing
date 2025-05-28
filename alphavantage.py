import json
from datetime import datetime

# Path to the JSON file
file_path = 'C:/Users/tabu9/PycharmProjects/pythonProject/articles_data_sainsb.json'

# New details
new_title = "New Title Example"
new_author = "N/A"
new_text = "New Title Example"  # Use the title as the text
new_url = "N/A"

# Get today's date in the required format
today_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

# Create a new dictionary with the details
new_article = {
    "title": new_title,
    "author": new_author,
    "date": today_date,
    "text": new_text,
    "url": new_url
}

# Load the existing data from the JSON file
with open(file_path, 'r') as file:
    articles = json.load(file)

# Append the new article to the list
articles.append(new_article)

# Write the updated list back to the JSON file
with open(file_path, 'w') as file:
    json.dump(articles, file, indent=4)

print(f"New article added successfully to {file_path}")
