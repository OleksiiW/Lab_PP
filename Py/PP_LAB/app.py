from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World! 24"


@app.route('/about')
def about():
    return "About page"


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
