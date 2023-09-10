from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/meniu/')
def meniu():
    return render_template("meniu.html")


if __name__ == '__main__':
    app.run(debug=True)
