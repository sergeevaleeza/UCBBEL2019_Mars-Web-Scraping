import sys
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import pymongo
import scrape_mars


# Create an instance of Flask
app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data

    # Run the scrape function
    mars_data_scrape = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, mars_data_scrape, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)