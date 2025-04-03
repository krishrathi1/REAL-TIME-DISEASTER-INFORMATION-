# Install required libraries
!pip install praw
!pip install requests
!pip install pandas
!pip install geopy
!pip install spacy
!pip install newsapi-python
!pip install vaderSentiment
!pip install pymongo
!pip install scikit-learn

# Import Libraries
import requests
import praw
import pandas as pd
import re
import uuid
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from geopy.geocoders import Nominatim
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
import spacy
import time
import json
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Load Spacy NLP model
nlp = spacy.load("en_core_web_sm")

# API Keys
REDDIT_CLIENT_ID = ""
REDDIT_CLIENT_SECRET = ""
REDDIT_USER_AGENT = ""
NEWSAPI_KEY = ""
WEATHER_API_KEY = ""
NASA_API_KEY = ""

# MongoDB Configuration
MONGO_URI = "mongodb+srv://manthangohil58:1zEuwkz2fg5FSlF1@cluster0.ltuiy.mongodb.net/"
DATABASE_NAME = "disaster_data_aman"
COLLECTION_NAME = "indian_updated_disaster_aman"

class RealTimeDisasterModel:
    def __init__(self, file_path):  # Fixed from _init_ to __init__
        self.file_path = file_path
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        self.newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
        self.geolocator = Nominatim(user_agent="disaster_monitor", timeout=10)
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.mongo_client = MongoClient(MONGO_URI)
        self.db = self.mongo_client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]
        self.vectorizer = CountVectorizer()
        self.model = LogisticRegression()

    def train_spam_detection_model(self):
        """Train a spam detection model using labeled data."""
        print("Training spam detection model...")
        # Example training data
        data = [
            {"text": "Flood in Assam causes massive destruction", "label": 1},
            {"text": "Earthquake in Delhi shakes buildings", "label": 1},
            {"text": "India launches new satellite", "label": 0},
            {"text": "Stock market crashes in the US", "label": 0},
        ]
        df = pd.DataFrame(data)
        X = self.vectorizer.fit_transform(df["text"])
        y = df["label"]
        self.model.fit(X, y)
        print("Spam detection model trained successfully.")

    def predict_relevance(self, text):
        """Predict whether a news item is relevant or spam."""
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]

    def fetch_reddit_data(self):
        """Fetch real-time disaster-related posts from Reddit."""
        print("Fetching disaster-related posts from Reddit...")
        disasters = []
        for subreddit in ["india", "indianews"]:
            try:
                for post in self.reddit.subreddit(subreddit).new(limit=50):
                    text = f"{post.title} {post.selftext}"
                    if any(keyword in text.lower() for keyword in ["flood", "earthquake", "cyclone", "landslide", "drought", "tsunami", "storm", "fire", "eruption"]):
                        disasters.append({
                            "title": post.title,
                            "description": post.selftext,
                            "postLink": f"https://reddit.com{post.permalink}",
                            "timestamp": datetime.fromtimestamp(post.created_utc).isoformat(),
                            "postAuthorURL": post.author.url if post.author else None
                        })
            except Exception as e:
                print(f"Error fetching data from Reddit: {e}")
        return disasters

    def fetch_newsapi_data(self):
        """Fetch real-time disaster-related news from NewsAPI."""
        print("Fetching disaster-related news from NewsAPI...")
        disasters = []
        try:
            response = self.newsapi.get_everything(
                q="(disaster OR flood OR earthquake OR cyclone OR landslide OR drought) AND India",
                language="en",
                from_param=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                sort_by="publishedAt"
            )
            for article in response["articles"]:
                if "India" in article["title"] or "India" in article["description"]:
                    disasters.append({
                        "title": article["title"],
                        "description": article["description"],
                        "postLink": article["url"],
                        "timestamp": article["publishedAt"],
                        "postAuthorURL": article["source"]["name"],
                        "imageURLS": [article["urlToImage"]] if article["urlToImage"] else ["https://via.placeholder.com/800x600.png?text=No+Image"]
                    })
        except Exception as e:
            print(f"Error fetching data from NewsAPI: {e}")
        return disasters

    def process_data(self, data):
        """Process and filter data using spam detection."""
        print("Processing data...")
        processed_data = []
        for item in data:
            text = f"{item.get('title', '')} {item.get('description', '')}"
            relevance = self.predict_relevance(text)
            notification = "yes" if relevance == 1 else "no"
            item["notification"] = notification
            if relevance == 1:  # Only process relevant news
                processed_data.append(item)
        return processed_data

    def save_to_mongodb(self, data):
        """Save relevant data to MongoDB."""
        print("Saving data to MongoDB...")
        try:
            self.collection.delete_many({})  # Clear existing data
            self.collection.insert_many(data)
            print("Data successfully saved to MongoDB.")
        except Exception as e:
            print(f"Error saving data to MongoDB: {e}")

    def evaluate_model(self):
        """Evaluate the spam detection model using a confusion matrix."""
        print("Evaluating spam detection model...")
        # Example test data
        test_data = [
            {"text": "Flood in Kerala causes destruction", "label": 1},
            {"text": "Cyclone hits Odisha coast", "label": 1},
            {"text": "India wins cricket match", "label": 0},
            {"text": "New technology launched in the US", "label": 0},
        ]
        df = pd.DataFrame(test_data)
        X_test = self.vectorizer.transform(df["text"])
        y_test = df["label"]
        y_pred = self.model.predict(X_test)
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

    def run(self):
        """Run the entire pipeline."""
        self.train_spam_detection_model()
        self.evaluate_model()
        while True:
            reddit_data = self.fetch_reddit_data()
            newsapi_data = self.fetch_newsapi_data()
            combined_data = reddit_data + newsapi_data
            relevant_data = self.process_data(combined_data)
            self.save_to_mongodb(relevant_data)
            print("Waiting for the next update cycle...")
            time.sleep(300)

# Run the model
if __name__ == "__main__":  # Fixed from _name_ to __name__
    model = RealTimeDisasterModel("/content/disasters_india.csv")
    model.run()
