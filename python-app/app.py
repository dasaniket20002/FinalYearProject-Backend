from flask import Flask
from routes import youtube

app = Flask(__name__)

app.add_url_rule('/', '', youtube.hello)

if __name__ == '__main__':
    app.run()