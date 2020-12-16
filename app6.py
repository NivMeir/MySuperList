from flask import Flask, render_template, request, redirect, url_for, flash
import DataBase

app = Flask(__name__)
users = DataBase.Users()


@app.route("/", methods = ["GET"])
def hello():
    return render_template("login.html")


#must be more then 8 chars, letters and numbers
def pass_check(password):
    if len(password) < 8:
        return False
    letter = False
    number = False
    for char in password:
        if str.isalpha(char):
            letter = True
        elif str.isalnum(char):
            number = True
    return letter and number


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        global name
        name = request.form.get("name")
        password = request.form.get("password")
        email = request.form.get("email")
        print(name , password , email)
        if users.email_isexist(email) or not pass_check(password):
            return render_template("failure.html")
        users.insert_user(email, password, name)
        return redirect(url_for('main'))

@app.route("/login", methods = ["POST"])
def login():
    global name
    name = "example"
    email = request.form.get("email")
    password = request.form.get("password")
    print(email , password)
    if not users.user_isexist(email, password):
        #flash('User was not found!')
        return render_template("failure.html")
    return redirect(url_for('main'))

@app.route("/main", methods = ["GET"])
def main():
    return render_template("main.html", name=name)

def creat_product(data, pname, pclass):
    product = {
        'pname': pname,
        'pclass': pclass,
    }
    data.append(product)
    return data

@app.route("/mysuperlist", methods = ["GET", "POST"])
def my_list():
    pname = "Banana"
    pclass = str(1)
    data = []
    data = creat_product(data, pname, pclass)
    pname = "apple"
    pclass = str(1)
    data = creat_product(data, pname, pclass)
    pname = "orange"
    pclass = str(1)
    for i in range(20):
        data = creat_product(data, pname, pclass)
    return render_template("mysuperlist.html", data = data)

@app.route("/allproducts", methods = ["GET", "POST"])
def all_products():
    if request.method == "GET":
        data = []
        pname = "apple"
        pclass = str(1)
        data = creat_product(data, pname, pclass)
        pname = "banana"
        pclass = str(1)
        data = creat_product(data, pname, pclass)
        pname = "orange"
        pclass = str(1)
        data = creat_product(data, pname, pclass)
        pname = "meat"
        pclass = str(3)
        data = creat_product(data, pname, pclass)
        pname = "chicken"
        pclass = str(3)
        data = creat_product(data, pname, pclass)
        pname = "fish"
        pclass = str(3)
        data = creat_product(data, pname, pclass)
        return render_template("allproducts.html", data = data)
    else:
        searched = request.args.get("search")
        print(searched)
        data =[]
        pname = "fish"
        pclass = str(3)
        data = creat_product(data, pname, pclass)
        return render_template("allproducts.html", data=data)

if __name__ == '__main__':
    app.run()
    #host='0.0.0.0' להתחברות ממכשירים אחרים אחרת לפחות מהפקודה למעלה