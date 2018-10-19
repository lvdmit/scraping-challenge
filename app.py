from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars


# Create an instance of our Flask app and Mongo.
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_app"
mongo = PyMongo(app)


from scrape_mars import scrape
@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)



@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    current_mars_data = scrape_mars.scrape()
    mars_data.update({}, current_mars_data, upsert=True)
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)
