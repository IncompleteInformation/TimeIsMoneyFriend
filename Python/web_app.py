from flask import Flask
app = Flask(__name__)


@app.route("/update")
def update():
    return "Hello World!"

if __name__ == "__main__":
    app.run()