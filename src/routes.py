from app import app
from flask import render_template, request, redirect
import db
import mainpage
import utils

@app.route("/")
def index():
    return mainpage.render()

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    address = request.form["address"]
    db.insert_restaurant(name, address)
    return redirect("/")

@app.route("/review/<int:id>")
def review(id):
    name = db.restaurant(id)
    categories = db.categories()
    return render_template("review.html", id=id, name=name, categories=categories)

@app.route("/result/<int:id>")
def result(id):
    name = db.restaurant(id)
    text_reviews = db.reviews(id)
    general_grade = db.rating(id)
    grades = utils.get_grades(id)
    return render_template("result.html", name=name, general_grade=general_grade, grades=grades, reviews=text_reviews)

@app.route("/answer", methods=["POST"])
def answer():
    restaurant = request.form["id"]
    review =request.form["review"]
    db.insert_review(review, restaurant)
    utils.insert_grades(restaurant)
    return redirect("/result/" + str(restaurant))