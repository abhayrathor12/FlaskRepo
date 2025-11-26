from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb+srv://Abhay:%40bhay2008@clusterflask.457nusr.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFlask")
db = client["test_db"]
collection = db["test_collection"]

@app.route('/api', methods=['GET'])
def get_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/')
def index():
    return render_template("index.html", error=None)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            return render_template("index.html", error="All fields are required!")

        # Insert into MongoDB
        collection.insert_one({
            "name": name,
            "email": email
        })

        return redirect(url_for("success"))

    except Exception as e:
        return render_template("index.html", error=str(e))

@app.route('/success')
def success():
    return render_template("success.html")


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8000)
