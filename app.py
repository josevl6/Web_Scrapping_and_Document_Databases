# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_data = mongo.db.mars.find_one()

    # return template and data
    return render_template("index.html", mars_data=mars_data)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    mars_data_scrape = scrape_mars.scrape_all()
    
    # Inserting mars_data into database
    # mongo.db.mars.update(mars_data_scrape)
    mongo.db.mars.insert_one(mars_data_scrape)
    # mongo.mars_db.mars_collection.update({}, mars_data_scrape, upsert=True)

    # Redirect back to home page
    # return redirect("/", code=302)
    return home()


if __name__ == "__main__":
    app.run(debug=True)