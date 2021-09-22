from flask import render_template
import db
import sys
import re

# For user to read in update_response.html.j2
errors = []

def handle_input(opening, closing, description, tag, id):
  
  input = {}
  log("INPUT")
  log(opening)
  log(closing)
  log(description)
  log(tag)
  log(id)
  log("/INPUT")

  #1. Validate input
  if validate_id(id):
    input["id"] = int(id)
    log("id is valid")
  else:
    return render_template("update_response.html.j2", errors=errors, id=id)
  if validate_time(opening):
    input["opening"] = opening
    log("opening is valid")
  if validate_time(closing):
    input["closing"] = closing
    log("closing is valid")
  if validate_description(description):
    input["description"] = description
    log("description is valid")
  if validate_tag(tag):
    input["tag"] = tag
    log("tag is valid")

  #2. Use data
  update(input)

  #3. User feedback
  log(errors)
  return render_template("update_response.html.j2", correct_input=input, id=id)

#Check if such restaurant exists
def validate_id(id):
  restaurant = db.select_restaurant(id)
  if restaurant:
    return True
  else:
    return False

# 24-hour format 
def validate_time(input):
  if input == "":
        return False
         
  regex = "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
  format = re.compile(regex)  
  k = re.search(format, input)

  if k is None :
    errors.append("Esitä aika 24 tunnin muodossa kuten 9:30 tai 22:00")
    return False
  else :
    return True

# No more than 1500 characters
def validate_description(input):
  if not input:
    return False

  value = str(input)
  if len(value) > 1500:
    errors.append("Ravintolan kuvaus on liian pitkä. Käytä enintään 1500 merkkiä")
    return False

  return True

# One word
def validate_tag(input):
  text = str(input)
  words = text.split()
  # empty input should not give error mesage to user
  if not input:
    return False

  if len(text) > 20 or len(words) > 1:
    errors.append("Tunnisteeksi kelpaa yksi sana, jonka pituus on max 20 merkkiä")
    return False
  return True

def update(input):
  log("UPDATE")
  try:
    db.update_info_opening(input["opening"], input["id"])
  except TypeError:
    pass
  except KeyError:
    pass
  try:
    db.update_info_closing(input["closing"], input["id"])
  except TypeError:
    pass
  except KeyError:
    pass
  try:
    db.update_info_description(input["description"], input["id"])
  except TypeError:
    pass
  except KeyError:
    pass
  tags = []
  try:
    tags = db.select_info_tags(input["id"])
    tags.append(input["tag"])
    db.update_info_tags(tags, input["id"])
  except TypeError:
    pass
  except KeyError:
    pass
  try:
    db.update_info_file(input["file"], input["id"])
  except TypeError:
    pass
  except KeyError:
    pass
  log("/UPDATE")
  


def log(m):
    print("LOG: " + str(m), file=sys.stdout)