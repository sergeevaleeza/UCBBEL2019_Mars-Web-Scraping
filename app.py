import os
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars_updated import scrape_all
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

app = Flask(__name__)

# Set up MongoDB configuration
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)

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

if __name__ == "__main__":
    app.run(debug=True)
