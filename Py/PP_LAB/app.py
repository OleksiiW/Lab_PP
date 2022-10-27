from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def hello_world():
    return "Home1"


@app.route('/about')
def about():
    return "About page"


if __name__ == "__main__":
    app.run(debug=True)
