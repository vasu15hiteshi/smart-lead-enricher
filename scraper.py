import requests
from bs4 import BeautifulSoup

def get_basic_info(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'
        return {"url": url, "title": title}
    except Exception as e:
        return {"url": url, "title": "Error"}