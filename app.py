# app.py
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_youtube():
    try:
        url = "https://www.youtube.com/results?search_query=flask+tutorials"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        videos = []
        
        for video in soup.find_all('a', {'id': 'video-title'}):
            video_title = video.get('title')
            video_link = "https://www.youtube.com" + video.get('href')
            if video_title:
                videos.append({'title': video_title, 'link': video_link})
        
        return videos
    except Exception as e:
        print(f"Error scraping YouTube: {e}")
        return []

def scrape_amazon():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = "https://www.amazon.com/s?k=laptop"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        for item in soup.select('.s-title span'):
            product_title = item.get_text().strip()
            products.append({'title': product_title})
        
        return products
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
        return []

@app.route('/')
def index():
    youtube_data = scrape_youtube()
    amazon_data = scrape_amazon()
    return render_template('index.html', youtube=youtube_data, amazon=amazon_data)

if __name__ == "__main__":
    app.run(debug=True)
