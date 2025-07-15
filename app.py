from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars_updated import scrape_all

app = Flask(__name__)

# Set up MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
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

if __name__ == "__main__":
    app.run(debug=True)
