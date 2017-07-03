from flask import Flask, render_template
from datetime import datetime
import spreadsheet_editor as se
import TimeIsMoneyFriend
from TimeIsMoneyFriend import AuctionHouse
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('front_page.html')


@app.route("/update")
def fetch_data():
    se.main()
    return "Updated Spreadsheet at " + str(datetime.now())[:-7]


# @app.route("/<server_slug>")
# def set_server(server_slug):


# @app.route("/item/<item_id>")
# def fetch_item_name(item_id):
#     return TimeIsMoneyFriend.item_db

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8083
    # app.debug = True
    app.run(host, port)
