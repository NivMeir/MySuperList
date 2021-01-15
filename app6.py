from flask import Flask, render_template, request, redirect, url_for, flash, session
import DataBase

app = Flask(__name__)
app.secret_key = "SuperList"
users = DataBase.Users()
mylist = DataBase.Mylist()
allproducts = DataBase.Allproducts()
global productlist
productlist = ["", "Fruits and Vegetables", "Drinks", "Meat, Chicken and Fish", "Bread", "Milk, Cheese and Eggs", "Snacks"]


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

@app.route("/forgotpassword", methods = ["GET", "POST"])
def newpassord():
    if request.method == 'GET':
        try:
            search = request.args.get("myemail")
            print(search, "123456789")
            if users.email_isexist(search):
                print("1234567890987654321")
            else:
                print("email do not exist")
        except:
            return render_template("forgotpassword.html" , check = 'False')
        return render_template("forgotpassword.html", check = 'True')

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
        data = mylist.get_my_products(session["userid"])
        return render_template("mysuperlist.html", data=data)
    elif request.method == 'POST':
        rowindex = request.form.get("rowindex")
        print(rowindex)

@app.route("/mysuperlist/delete/<product>", methods = ["GET"])
def delete_product(product):
    if request.method == 'GET':
        print(product, "122243434")
        mylist.delete_product(product, session['userid'])
        return redirect('/mysuperlist')

def get_location_num(locatuonname):
    for i in range(len(productlist)):
        if locatuonname == productlist[i]:
            return i

#productlist = ["", "Fruits and Vegetables", "Drinks", "Meat, Chicken and Fish", "Bread", "Milk, Cheese and Eggs",
               #"Snacks"]
@app.route("/allproducts", methods = ["GET", "POST"])
def all_products():
    if request.method == "GET":
        """
        allproducts.insert_product("apple", get_location_num("Fruits and Vegetables"),"Fruits and Vegetables" )
        allproducts.insert_product("banana", get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
        allproducts.insert_product("orange", get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
        allproducts.insert_product("strawberry", get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
        allproducts.insert_product("grapes", get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
        allproducts.insert_product("watermelon", get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
        allproducts.insert_product("potato", get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
        allproducts.insert_product("onion", get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
        allproducts.insert_product("tomato", get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
        allproducts.insert_product("cucumber", get_location_num("Fruits and Vegetables"), "Fruits and Vegetables")
        allproducts.insert_product("coca cola", get_location_num("Drinks"), "Drinks")
        allproducts.insert_product("sprite", get_location_num("Drinks"), "Drinks")
        allproducts.insert_product("fanta", get_location_num("Drinks"), "Drinks")
        allproducts.insert_product("orange juice", get_location_num("Drinks"), "Drinks")
        allproducts.insert_product("beer", get_location_num("Drinks"), "Drinks")
        allproducts.insert_product("red wine", get_location_num("Drinks"), "Drinks")
        allproducts.insert_product("water", get_location_num("Drinks"), "Drinks")
        allproducts.insert_product("white wine", get_location_num("Drinks"), "Drinks")
        allproducts.insert_product("bakala fish", get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
        allproducts.insert_product("salmon", get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
        allproducts.insert_product("chicken Breast", get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
        allproducts.insert_product("chicken thighs", get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
        allproducts.insert_product("entrecote", get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
        allproducts.insert_product("ground beef", get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
        allproducts.insert_product("sausage", get_location_num("Meat, Chicken and Fish"), "Meat, Chicken and Fish")
        allproducts.insert_product("pita", get_location_num("Bread"), "Bread")
        allproducts.insert_product("bread", get_location_num("Bread"), "Bread")
        allproducts.insert_product("cream cheese", get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
        allproducts.insert_product("yellow cheese ", get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
        allproducts.insert_product("yogurt", get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
        allproducts.insert_product("mozzarella cheese", get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
        allproducts.insert_product("cottage cheese", get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
        allproducts.insert_product("eggs", get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
        allproducts.insert_product("milk", get_location_num("Milk, Cheese and Eggs"), "Milk, Cheese and Eggs")
        allproducts.insert_product("bamba", get_location_num("Snacks"), "Snacks")
        allproducts.insert_product("chips", get_location_num("Snacks"), "Snacks")
        allproducts.insert_product("pretzels", get_location_num("Snacks"), "Snacks")
        allproducts.insert_product("cornflaxes", get_location_num("Snacks"), "Snacks")"""
        try:
            search = request.args.get("search")
            print(search, "123456789")
        except:
            print("wasn't found")
        data = allproducts.get_products(search)
        print(data)
        return render_template("allproducts.html", data = data)

@app.route("/allproducts/insert/<product>", methods = ["GET", "POST"])
def insert_product(product):
    if request.method == 'GET':
        print(product, "122243434")
        info = allproducts.get_product_info(product)
        print(info, "2323232323232")
        mylist.insert_product(info[0], info[2], info[1], session['userid'])
        return redirect('/allproducts')




if __name__ == '__main__':
    app.run(port= 80)
    #host='0.0.0.0' להתחברות ממכשירים אחרים אחרת לפחות מהפקודה למעלה