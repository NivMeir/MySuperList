from flask import Flask, render_template, request, redirect, url_for, flash, session
import DataBase

app = Flask(__name__)
users = DataBase.Users()
mylist = DataBase.Mylist()
app.secret_key = "SuperList"

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
        try:
            name = request.form.get("name")
            password = request.form.get("password")
            email = request.form.get("email")
            print(name , password , email)
            if users.email_isexist(email) or not pass_check(password):
                return render_template("failure.html")
            users.insert_user(email, password, name)
            userid = users.get_user_id(email)
            print(userid)
            session['userid'] = userid
            return redirect(url_for('main'))
        except:
            return render_template("register.html")

@app.route("/login", methods = ["POST"])
def login():
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        print(email , password)
        if not users.user_isexist(email, password):
            #flash('User was not found!')
            return render_template("failure.html")
        userid = users.get_user_id(email)
        session['userid'] = userid
        return redirect(url_for('main'))
    except:
        return render_template("login.html")

@app.route("/main", methods = ["GET"])
def main():
    if 'userid' in session:
        id = session['userid']
    name = users.get_user_name(id)
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
    if request.method == 'GET':
        mylist.insert_product("banana", 1, 'fruits', 1)
        mylist.insert_product("apple", 1, 'fruits', 1)
        data = mylist.get_my_products(session["userid"])
        return render_template("mysuperlist.html", data=data)
    elif request.method == 'POST':
        rowindex = request.form.get("rowindex")
        print(rowindex)

@app.route("/allproducts", methods = ["GET", "POST"])
def all_products():
    if request.method == "GET":
        data = []
        pname = "apple"
        pclass = "fruits"
        data = creat_product(data, pname, pclass)
        pname = "banana"
        pclass = "fruits"
        data = creat_product(data, pname, pclass)
        pname = "orange"
        pclass = "fruits"
        data = creat_product(data, pname, pclass)
        pname = "meat"
        pclass = "Meat and fish"
        data = creat_product(data, pname, pclass)
        pname = "chicken"
        pclass ="Meat and fish"
        data = creat_product(data, pname, pclass)
        pname = "fish"
        pclass = "Meat and fish"
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
    app.run(port= 80)
    #host='0.0.0.0' להתחברות ממכשירים אחרים אחרת לפחות מהפקודה למעלה