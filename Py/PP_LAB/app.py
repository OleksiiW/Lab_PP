from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def hello_world():
    return render_template("index.html")


@app.route('/about')
def about():
    return "About page"


if __name__ == "__main__":
    app.run(debug=True)
