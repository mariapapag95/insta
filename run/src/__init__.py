from flask import Flask
from src import controller
app = Flask(__name__)
app.secret_key = "maria"