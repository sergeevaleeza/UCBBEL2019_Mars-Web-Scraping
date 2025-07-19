import os
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars_updated import scrape_all
from dotenv import load_dotenv

# for self-ping
import threading
import time
import requests
from datetime import datetime

# Load .env from the secret file path
load_dotenv('/etc/secrets/.env')
# load_dotenv('.env')

app = Flask(__name__)

# Set up MongoDB configuration
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
#MONGO_URI = os.getenv("MONGO_URI")
#app.config["MONGO_URI"] = MONGO_URI

mongo = PyMongo(app)

def self_ping():
    """Ping the app every 14 minutes to prevent sleeping"""
    while True:
        try:
            time.sleep(14 * 60)  # Wait 14 minutes
            response = requests.get('https://mars-info-web-scraping.onrender.com/')
            print(f"Self-ping successful at {datetime.now()}: {response.status_code}")
        except Exception as e:
            print(f"Self-ping failed at {datetime.now()}: {e}")

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    # Scrape new data
    mars_data = scrape_all()
    
    # Update MongoDB with new data
    mongo.db.mars_data.update_one({}, {"$set": mars_data}, upsert=True)
    
#    print("Scraped Data:\n", mars_data)  # Debug output to verify
    return redirect("/", code=302)

@app.route("/healthz")
def health():
    return "OK", 200

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

if __name__ == "__main__":
    ping_thread = threading.Thread(target=self_ping, daemon=True)
    ping_thread.start()
    
    app.run(host='0.0.0.0', port=10000, debug=True)  # Your existing Flask run code
