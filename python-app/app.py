from flask import Flask
from routes import youtube
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
PORT = os.getenv('PORT')

app.add_url_rule(rule='/', methods=['GET'], view_func=youtube.hello)
app.add_url_rule(rule='/trending', methods=['GET'], view_func=youtube.getTrending)

if __name__ == '__main__':
    app.run(port=PORT)