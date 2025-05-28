import requests
from lxml import html
from datetime import datetime, timedelta

# Define the URL
url = 'https://news.google.com/search?q=sainsburys&hl=en-GB&gl=GB&ceid=GB%3Aen'

# Make a request to the website
response = requests.get(url)

# Parse the page content
tree = html.fromstring(response.content)

# Define the XPaths
title_xpath = "//div[@class='UW0SDc']//a//text()"
time_xpath = "//div[@class='UW0SDc']//time//text()"

# Extract data using XPath
titles = tree.xpath(title_xpath)
times = tree.xpath(time_xpath)


# Helper function to format dates
def format_time(time_str):
    time_str = time_str.strip()

    if time_str.lower() == 'yesterday':
        return (datetime.now() - timedelta(days=1)).strftime('%d %b %Y')

    if 'hours ago' in time_str:
        hours_ago = int(time_str.split()[0])
        return (datetime.now() - timedelta(hours=hours_ago)).strftime('%d %b %Y')

    if 'days ago' in time_str:
        days_ago = int(time_str.split()[0])
        return (datetime.now() - timedelta(days=days_ago)).strftime('%d %b %Y')

    # Handle dates in 'd MMM' format (e.g., '13 Jul')
    try:
        return datetime.strptime(time_str, '%d %b').replace(year=datetime.now().year).strftime('%d %b %Y')
    except ValueError:
        # Handle dates in 'd MMM yyyy' format (e.g., '9 Dec 2023')
        try:
            return datetime.strptime(time_str, '%d %b %Y').strftime('%d %b %Y')
        except ValueError:
            return time_str  # Return the original string if parsing fails


# Combine titles and times into a list of tuples
results = list(zip(titles, times))

