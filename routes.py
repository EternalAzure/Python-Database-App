from app import app
from flask import render_template, request, redirect, session, flash
import db
import mainpage
import utils
import update_info
import register as r
import login as l
import sys


# IMAGE
@app.route("/send", methods=["POST"])
def send():
    file = request.files["file"]
    name = file.filename
    r_id = request.form["restaurant_id"]
    if not name.endswith(".jpg"):
        flash('Kelvoton tiedostonimi. Käytä .jpg')
        return redirect(request.referrer)
    data = file.read()
    if len(data) > 100*1024:
        return "Too big file"
    db.insert_image(name, data, r_id)
    flash("Kuva ladattiin onnistuneesti")
    return redirect(request.referrer)

@app.route("/show/<int:id>")
def show(id):
    image = db.select_image(id)
    if image:return image
    return "No image"

@app.route("/foo")
def foo():
    return render_template("mat_form.html")
# /IMAGE

def log(m):
    print("LOG: " + str(m), file=sys.stdout)

@app.route("/")
def index():
    return mainpage.render()

@app.route("/new")
def new():
    return render_template("new.html.j2")

@app.route("/restaurant/<int:id>", methods=["GET"])
def restaurant(id):
    data = db.select_restaurant(id)
    info = db.select_info_all(id)
    info = utils.stringify(info)
    return render_template("info.html.j2", data=data, info=info, id=id)

@app.route("/review/<int:id>")
def review(id):
    name = db.select_restaurant(id).name
    categories = db.categories()
    return render_template("review.html.j2", id=id, name=name, categories=categories)

@app.route("/result/<int:id>")
def result(id):
    name = db.select_restaurant(id).name
    text_reviews = list(db.select_reviews(id))
    text_reviews.reverse()
    general_grade = db.grades_full_summary(id)
    grades = db.grades_partial_summary(id)
    return render_template("result.html.j2", name=name, general_grade=general_grade, grades=grades, reviews=text_reviews, id=id)
      
@app.route("/login_page") 
def login_page():
    return render_template("login_page.html.j2")

@app.route("/register_page")
def register_page():
    return render_template("register_page.html.j2")

@app.route("/delete_restaurant/<int:id>")
def delete_restaurant(id):
    db.delete_restaurant(id)
    return redirect("/")

@app.route("/delete_review/<int:id>", methods=["POST"])
def delete_review(id):
    review_id = request.form["review_id"]
    db.delete_review(review_id)
    return redirect("/result/"+str(id))

@app.route("/api/restaurants", methods=["GET"])
def restaurants():
    return utils.json_restaurants()

@app.route("/update_info", methods=["POST"])
def update():
    opening = request.form["opening"]
    closing = request.form["closing"]
    description = request.form["description"]
    tag = request.form["tag"]
    id = request.form["id"]
    return update_info.handle_input(opening, closing, description, tag, id)

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    street = request.form["street"]
    city = request.form["city"]
    #Validate address
    #m.location(city, street)
    #
    #
    restaurant_id = db.insert_restaurant(name, street, city)
    db.insert_info_all(None, None, "", [], restaurant_id)
    return redirect("/")

@app.route("/answer", methods=["POST"])
def answer():
    restaurant = request.form["id"]
    review =request.form["review"]
    db.insert_review(review, restaurant)
    utils.insert_grades(restaurant)
    return redirect("/result/" + str(restaurant))

@app.route("/register", methods=["POST"])
def register():
    return r.register()


@app.route("/login",methods=["POST"])
def login():
    return l.login()

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
