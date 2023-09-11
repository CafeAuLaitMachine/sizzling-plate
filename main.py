from flask import Flask, render_template
import json

app = Flask(__name__)
menu_dict = json.load(open("menu.json"))


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/menu')
def menu():
    return render_template("menu.html", menu=menu_dict)


if __name__ == '__main__':
    app.run(debug=True)
