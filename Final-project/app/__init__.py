from flask import Flask
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



from app import auth, main, shop, checkout,cart,user,wishlist