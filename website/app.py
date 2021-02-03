from re import sub
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

# fancy magic for configs
load_dotenv()
app = Flask(__name__)
# Set DEBUG False in .env for deployment!!!
if os.environ["DEBUG"] == "True":
    SECRET_KEY = "DEV"
else:
    SECRET_KEY = os.environ["SECRET_KEY"]
DATABASE_URL = os.environ["DB_URL"]
API_KEY = os.environ["API_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config.update(SECRET_KEY=SECRET_KEY)
csrf = CSRFProtect()  # register csrf protection
csrf.init_app(app)  # activate it
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class PersonModel(db.Model):
    __tablename__ = "Persons"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    hobby = db.Column(db.Integer)
    sub_cult = db.Column(db.Integer)
    outdoor = db.Column(db.Integer)
    description = db.Column(db.String)

    def __init__(self, username, email, hobby, sub_cult, outdoor, description):
        self.username = username
        self.email = email
        self.hobby = hobby
        self.sub_cult = sub_cult
        self.outdoor = outdoor
        self.description = description


# create person entry
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        hobby = request.form["hobby"]
        sub_cult = request.form["subcult"]
        outdoor = request.form["outdoor"]
        description = request.form["description"]
        person = PersonModel(
            username=username,
            email=email,
            hobby=hobby,
            sub_cult=sub_cult,
            outdoor=outdoor,
            description=description,
        )
        db.session.add(person)
        db.session.commit()
        return render_template("success.html")
    else:
        response = render_template("index.html")
        return response


# get all results
@app.route("/api/all", methods=["GET"])
def handle_all():
    key = request.headers["api_key"]
    if key == API_KEY:
        persons = PersonModel.query.all()
        result = [
            {
                "id": person.id,
                "username": person.username,
                "email": person.email,
                "hobby": person.hobby,
                "sub_cult": person.sub_cult,
                "outdoor": person.outdoor,
                "descrption": person.description,
            }
            for person in persons
        ]
        return {"count": len(result), "persons": result}
    else:
        return "missing api key", 403


@app.route("/api/person/<person_id>", methods=["GET"])
def persons_handler(person_id):
    person = PersonModel.query.get_or_404(person_id)
    if request.method == "GET":
        key = request.headers["api_key"]
        if key == API_KEY:
            result = {
                "id": person.id,
                "username": person.username,
                "email": person.email,
                "hobby": person.hobby,
                "sub_cult": person.sub_cult,
                "outdoor": person.outdoor,
                "descrption": person.description,
            }
            return {"message": "success", "result": result}
        else:
            return "missing api key", 403


if __name__ == "__main__":
    app.run()