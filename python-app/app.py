from flask import Flask
from flask_cors import CORS
from routes import youtube
from utils import consts

app = Flask(__name__)
CORS(app)

app.add_url_rule(rule='/youtube/trending', methods=['GET'], view_func=youtube.getTrending)
app.add_url_rule(rule='/youtube/trending/page', methods=['GET'], view_func=youtube.getPagedTrending)
app.add_url_rule(rule='/youtube/search', methods=['GET'], view_func=youtube.getSearch)
app.add_url_rule(rule='/youtube/search/page', methods=['GET'], view_func=youtube.getPagedSearch)

if __name__ == '__main__':
    app.run(port=consts.PORT)
    