from flask import Flask
from datetime import datetime
import spreadsheet_editor as se
app = Flask(__name__)


@app.route("/")
def index():
    return "Append /update to URL to fetch AH data."


@app.route("/update")
def fetch_data():
    se.main()
    return "Updated Spreadsheet at " + str(datetime.now())[:-7]

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8083
    # app.debug = True
    app.run(host, port)
