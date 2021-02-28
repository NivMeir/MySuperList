from flask import Flask, render_template, request, redirect, url_for, flash, session
import DataBase
import emails

app = Flask(__name__)
app.secret_key = "SuperList"
send_email = emails.Emails()
users = DataBase.Users()
mylist = DataBase.Mylist()
allproducts = DataBase.Allproducts()
global productlist
productlist = ["", "Fruits and Vegetables", "Drinks", "Meat, Chicken and Fish", "Bread", "Milk, Cheese and Eggs", "Snacks"]

@app.route("/", methods = ["GET"])
def hello():
    """
    send the login page to the user
    rtype: html page
    """
    return render_template("login.html")


#must be more then 8 chars, letters and numbers
def pass_check(password):
    """
    check the password, it has to be more then 8 chars, letters and numbers
    param password: the user password that he want to register with
    type: string
    return: checks that the password received is conditional
    rtype: boolean
    """
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
    """
    GET:
    retrun the register page
    rtype: html page
    POST:
    get the user information and write them at the database if they meet the requirements
    return the register page if the information from the user is incorrect, otherwise return the path to the next page
    rtype: html page or url path
    """
    if request.method == 'GET':
        return render_template("register.html")
    else:
        try:
            name = request.form.get("name")
            password = request.form.get("password")
            email = request.form.get("email")
            print(name , password , email)
            if users.email_isexist(email):
                flash("The Email Is Already In The System")
                return render_template("register.html")
            elif not pass_check(password):
                flash("The Password Must Have 8 Chars, Letters And Numbers")
                return render_template("register.html")
            elif len(name) > 10 or len(name) < 2:
                flash("Your Name Has To Be Between 2 Chars To 10!")
                return render_template("register.html")
            users.insert_user(email, password, name)
            userid = users.get_user_id(email)
            print(userid)
            session['userid'] = userid
            return redirect(url_for('main'))
        except:
            return render_template("register.html")

@app.route("/login", methods = ["POST"])
def login():
    """
        get the user information and check them at the database if they meet the requirements
        return the login page if the information from the user is incorrect, otherwise return the path to the next page
        rtype: html page or url path
        """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        print(email , password)
        if not users.user_isexist(email, password):
            flash('User was not found!')
            return render_template("login.html")
        userid = users.get_user_id(email)
        session['userid'] = userid
        return redirect(url_for('main'))
    except:
        return render_template("login.html")


@app.route("/forgotpass", methods = ["GET", "POST"])
def forgotpass():
    """
        GET:
        retrun the forgotpass page
        rtype: html page
        POST:
        get the user's email and check it at the database if it exist, and then send a code to their email
        return the forgotpass page if the information from the user is incorrect, otherwise return the path to the next page
        rtype: html page or url path
        """
    if request.method == 'GET':
        return render_template("forgotpass.html")
    elif request.method == 'POST':
        try:
            email = request.form.get("email")
            if email != None and users.email_isexist(email):
                session["userid"] = users.get_user_id(email)
                username = users.get_user_name(session["userid"])
                code = send_email.codegenerator(username)
                session["code"] = code
                send_email.send_email(email, code)
                return redirect(url_for('mailcode'))
            else:
                flash("Email Was Not Found")
                return render_template("forgotpass.html")
        except:
            return render_template("forgotpass.html")
    else:
        print("done forgot password")


@app.route("/mailcode", methods=["GET", "POST"])
def mailcode():
    """
    GET:
    retrun the mailcode page
    rtype: html page
    POST:
    get the user's code and check it
    return the forgotpass page if the code from the user is incorrect, otherwise return the path to the next page
    rtype: html page or url path
    """
    if request.method == 'GET':
        return render_template("mailcode.html")
    elif request.method == 'POST':
        try:
            code = request.form.get("code")
            if code != None and code == session["code"]:
                return redirect(url_for('changepassword'))
            else:
                flash("Wrong Code")
                return render_template("mailcode.html")
        except:
            return render_template("mailcode.html")
    else:
        print("done mail code")


@app.route("/changepassword", methods=["GET", "POST"])
def changepassword():
    """
    GET:
    retrun the changepassword page
    rtype: html page
    POST:
    get the user's new password, if it meet the requirements the password is changing at the database
    return the changepassword page if the password from the user is incorrect, otherwise return the path to the next page
    rtype: html page or url path
    """
    if request.method == 'GET':
        return render_template("changepassword.html")
    elif request.method == 'POST':
        try:
            newpass = request.form.get("newpass")
            email = users.get_user_email(session["userid"])
            if newpass != None and pass_check(newpass):
                users.update_password(email, newpass)
                return redirect(url_for('main'))
            else:
                flash("The Password Must Have 8 Chars, Letters And Numbers")
                return render_template("changepassword.html")
        except:
            print("something went wrong")
            return render_template("changepassword.html")
    else:
        print("done change password")


@app.route("/main", methods = ["GET"])
def main():
    id = ''
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
        data = mylist.get_my_products(session["userid"])
        return render_template("mysuperlist.html", data=data)

@app.route("/mysuperlist/delete/<product>", methods = ["GET"])
def delete_product(product):
    if request.method == 'GET':
        mylist.delete_product(product, session['userid'])
        flash(product + " Has Been Deleted From Your Super List")
    return redirect('/mysuperlist')



def insertproducts():
    allproducts.insert_product("apple", 'A', get_location_num("Fruits and Vegetables"),"Fruits and Vegetables" )
    allproducts.insert_product("banana", 'A',get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
    allproducts.insert_product("orange", 'A',get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
    allproducts.insert_product("strawberry", 'B',get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
    allproducts.insert_product("grapes", 'B',get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
    allproducts.insert_product("watermelon", 'B',get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
    allproducts.insert_product("potato", 'C',get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
    allproducts.insert_product("onion", 'C',get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
    allproducts.insert_product("tomato", 'C',get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
    allproducts.insert_product("cucumber", 'C',get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
    allproducts.insert_product("coca cola", 'A',get_location_num("Drinks"), "Drinks")
    allproducts.insert_product("sprite", 'A',get_location_num("Drinks"), "Drinks")
    allproducts.insert_product("fanta", 'B',get_location_num("Drinks"), "Drinks")
    allproducts.insert_product("orange juice", 'B',get_location_num("Drinks"), "Drinks")
    allproducts.insert_product("beer", 'C',get_location_num("Drinks"), "Drinks")
    allproducts.insert_product("red wine", 'C',get_location_num("Drinks"), "Drinks")
    allproducts.insert_product("water", 'D',get_location_num("Drinks"), "Drinks")
    allproducts.insert_product("white wine", 'D',get_location_num("Drinks"), "Drinks")
    allproducts.insert_product("bakala fish", 'A',get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
    allproducts.insert_product("salmon", 'A',get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
    allproducts.insert_product("chicken Breast", 'A',get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
    allproducts.insert_product("chicken thighs", 'B',get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
    allproducts.insert_product("entrecote", 'B',get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
    allproducts.insert_product("ground beef", 'B',get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
    allproducts.insert_product("sausage", 'B',get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
    allproducts.insert_product("pita", 'A',get_location_num("Bread"), "Bread")
    allproducts.insert_product("bread", 'A',get_location_num("Bread"), "Bread")
    allproducts.insert_product("cream cheese", 'A',get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
    allproducts.insert_product("yellow cheese", 'A',get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
    allproducts.insert_product("yogurt", 'B',get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
    allproducts.insert_product("mozzarella cheese", 'B',get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
    allproducts.insert_product("cottage cheese", 'C',get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
    allproducts.insert_product("eggs", 'C',get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
    allproducts.insert_product("milk", 'C',get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
    allproducts.insert_product("bamba", 'A',get_location_num("Snacks"), "Snacks")
    allproducts.insert_product("chips", 'A',get_location_num("Snacks"), "Snacks")
    allproducts.insert_product("pretzels", 'B',get_location_num("Snacks"), "Snacks")
    allproducts.insert_product("cornflaxes", 'B',get_location_num("Snacks"), "Snacks")

@app.route("/allproductsmenu", methods = ["GET"])
def all_products_menu():
    if request.method == "GET":
        #insertproducts()
        return render_template("mainproducts.html")

@app.route("/allproductsmenu/<department>", methods = ["GET"])
def choose_department(department):
    if request.method == 'GET':
        data = allproducts.get_products(department)
        search = ""
        try:
            search = request.args.get("search")
        except:
            print("Wasn't Found")
        if search != None:
            data = allproducts.get_products(search)
        return render_template("allproducts.html", data=data)

@app.route("/allproductsmenu/<department>/insert/<product>", methods = ["GET", "POST"])
def insert_products(department, product):
    if request.method == 'GET':
        info = allproducts.get_product_info(product)
        print(info)
        if info != False:
            mylist.insert_product(info[0], info[2], info[1], info[3], session['userid'])
            flash(product + " Has Been Added To Your Super List")
        else:
            print("the product was not found")
        url = '/allproductsmenu/' + str(department)
        return redirect(url)

def get_location_num(locatuonname):
    for i in range(len(productlist)):
        if locatuonname == productlist[i]:
            return i


"""
@app.route("/allproducts", methods = ["GET", "POST"])
def all_products():
    if request.method == "GET":
        #insertproducts()
        search = ""
        try:
            search = request.args.get("search")
        except:
            print("wasn't found")
        data = allproducts.get_products(search)
        return render_template("allproducts.html", data = data)

@app.route("/allproducts/insert/<product>", methods = ["GET", "POST"])
def insert_product(product):
    if request.method == 'GET':
        info = allproducts.get_product_info(product)
        mylist.insert_product(info[0], info[2], info[1], session['userid'])
        return redirect('/allproducts')
"""

if __name__ == '__main__':
    app.run(port= 80)
    #host='0.0.0.0' להתחברות ממכשירים אחרים אחרת לפחות מהפקודה למעלה