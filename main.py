from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)
menu_dict = json.load(open("menu.json"))


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/menu', methods=["POST", "GET"])
def menu():
    return render_template("menu.html", menu=menu_dict)


@app.route('/checkout/<string:dish>', methods=["POST", "GET"])
@app.route('/checkout')
def checkout(dish=None, menu=menu_dict):
    for food in menu:
        if food['item'] == dish:
            chosen_food = food
    if request.method == 'POST':
        client = dict()
        client["name"] = request.form['nm']
        client["surname"] = request.form['srn']
        client["gmail"] = request.form['gmail']
        client["order"] = chosen_food
        return redirect('/confirmation/' + json.dumps(client))
    else:
        return render_template("checkout.html", dish=chosen_food)


@app.route('/confirmation/<string:client>')
def confirm(client):
    return render_template("con_page.html", client=json.loads(client))


if __name__ == '__main__':
    app.run(debug=True)
