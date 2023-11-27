from flask import Flask, render_template, request, redirect, session
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

app = Flask(__name__)
menu_dict = json.load(open("menu.json"))
app.secret_key = "C0ck"


@app.route('/add/')
@app.route('/add/<string:dishes>')
def add_to_cart(dishes=None):
    if dishes is not None:
        if "dishes" not in session:
            session["dishes"] = json.loads(dishes)
        else:
            session["dishes"] = session["dishes"] + json.loads(dishes)
    return redirect("/checkout/")


def send_email(client):
    sender = 'sizzling.plate.restoraunt@zohomail.eu'
    sender_title = "Sizzling Plate"
    recipient = client['email']
    order = ""
    for dish in client['order']['items']:
        order += (dish + " x1" + '\n')

    msg = MIMEText(
        f"You have ordered: "
        f"{order}"
        f""
        f"In total {client['order']['price']}$", 'plain', 'utf-8')
    msg['Subject'] = Header("meow meow", 'utf-8')
    msg['From'] = formataddr((str(Header(sender_title, 'utf-8')), sender))
    msg['To'] = recipient

    server = smtplib.SMTP_SSL('smtp.zoho.eu', 465)
    server.login('sizzling.plate.restoraunt@zohomail.eu', 'KpKU37xCeX4r')
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/menu/', methods=["GET"])
def menu():
    return render_template("menu.html", menu=menu_dict)


@app.route('/checkout/', methods=["POST", "GET"])
def checkout(menu=menu_dict):
    total = 0
    if "dishes" in session:
        for dish in session["dishes"]:
            for food in menu:
                if food['item'] == dish:
                    total += food['price']
                    break
        dishes = session["dishes"]
        if request.method == 'POST':
            client = {"name": request.form['name'], "surname": request.form['surname'], "email": request.form['email'],
                      "order": {'price': total, 'items': session["dishes"]}}
            session['client'] = client
            return redirect('/confirmation')
    else:
        dishes = []
    return render_template("checkout.html", dishes=dishes, total=total)


@app.route('/confirmation')
def confirm():
    if "client" in session:
        client = session['client']
        send_email(client)
        session.clear()
        return render_template("confirm_page.html", client=client)
    else:
        return redirect("/checkout")

if __name__ == '__main__':
    app.run(debug=True)
