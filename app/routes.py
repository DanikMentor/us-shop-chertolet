from flask import render_template
from app import app

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/register")
def register():
    return render_template("register.html")

    login = request.form["name"]
    mail = request.form["email"]
    phone = request.form["phone"]
    password = request.form["password"]

    add_user_to_db(login, password, mail, phone)
    

if __name__ == "__main__":
    app.run(debug=True)