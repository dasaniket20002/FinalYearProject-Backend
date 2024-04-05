from flask import Flask
from flask_cors import CORS

from routes import youtube, signin, db_ops
from utils import consts

app = Flask(__name__)
CORS(app)

app.add_url_rule(rule='/youtube/trending', methods=['GET'], view_func=youtube.getTrending)                              # PARAMS - access_token, token_type, region_code 
app.add_url_rule(rule='/youtube/trending/page', methods=['GET'], view_func=youtube.getPagedTrending)                    # PARAMS - access_token, token_type, region_code, page_token
app.add_url_rule(rule='/youtube/search', methods=['GET'], view_func=youtube.getSearch)                                  # PARAMS - access_token, token_type, region_code 
app.add_url_rule(rule='/youtube/search/page', methods=['GET'], view_func=youtube.getPagedSearch)                        # PARAMS - access_token, token_type, region_code, page_token
app.add_url_rule(rule='/youtube/getAllRecommendations', methods=['GET'], view_func=youtube.getAllRecommendations)       # PARAMS - access_token, token_type, region_code | POST - sub

app.add_url_rule(rule='/signin', methods=['POST'], view_func=signin.signin)                                             # POST - sub
app.add_url_rule(rule='/update', methods=['POST'], view_func=db_ops.update_user_data)                                   # POST - sub, channel, tags, topics

if __name__ == '__main__':
    app.run(port=consts.PORT)
    