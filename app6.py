from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def hello():
    return render_template("login.html")


@app.route("/register", methods = ["GET" , "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        global name
        name = request.form.get("name")
        password = request.form.get("password")
        email = request.form.get("email")
        print(name , password , email)
        if not name or not password or not email:
            return render_template("failure.html")
        return redirect(url_for('main'))

@app.route("/login", methods = ["POST"])
def login():
    global name
    name = "example"
    email = request.form.get("email")
    password = request.form.get("password")
    print(email , password)
    if not email or not password:
        return render_template("failure.html")
    return redirect(url_for('main'))

@app.route("/main", methods = ["GET", "POST"])
def main():
    #name = "niv"
    return render_template("main.html", name=name)


@app.route("/mysuperlist", methods = ["GET"])
def my_list():
    if request.method == "GET":
        pname = "Banana"
        pclass = str(1)
        data = []
        product = {
                'pname': pname,
                'pclass': pclass,
            }
        data.append(product)
        data.append(product)
        data.append(product)
        pname = "apple"
        pclass = str(1)
        product = {
            'pname': pname,
            'pclass': pclass,
        }
        data.append(product)
        data.append(product)
        pname = "orange"
        pclass = str(1)
        product = {
            'pname': pname,
            'pclass': pclass,
        }
        data.append(product)
        data.append(product)
        return render_template("mysuperlist.html", data = data)
    else:
        return redirect(url_for('main'))

@app.route("/allproducts", methods = ["GET"])
def all_products():
    return render_template("failure.html")

if __name__ == '__main__':
    app.run()