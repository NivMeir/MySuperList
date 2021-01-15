import sqlite3

class Users:
    """Creates database with users table includes:
       create query
       insert query
       select query
    """

    def __init__(self, tablename="users", userid = "userid", email="email", password="password", username="username"):
        self.__tablename = tablename
        self.__userid = userid
        self.__email = email
        self.__password = password
        self.__username = username
        conn = sqlite3.connect('Super_List_Data_Base.db')
        print("Opened database successfully")
        id = str(self.__userid)
        query_str = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + id + " INTEGER,"
        query_str += " " + self.__email + " TEXT NOT NULL UNIQUE,"
        query_str += " " + self.__password + " TEXT NOT NULL,"
        query_str += " " + self.__username + " TEXT NOT NULL,"
        query_str += " " +"PRIMARY KEY(" + id + " AUTOINCREMENT" + "));"
        conn.execute(query_str)
        print("Users table created successfully")
        """
        strsql = "SELECT userid FROM users " + \
                 "INNER JOIN users on user.userid = mylist.userid;"
        print(strsql)
        conn.execute(strsql)       
        """
        conn.commit()
        conn.close()

    def __str__(self):
        return "table  name is ", self.__tablename

    def get_table_name(self):
        return self.__tablename

    def get_user_id(self, email):
        if self.email_isexist(email):
            conn = sqlite3.connect('Super_List_Data_Base.db')
            strsql = "SELECT * from " + self.__tablename + ";"
            print(strsql)
            cursor = conn.execute(strsql)
            for row in cursor:
                if email == row[1]:
                    return row[0]
        else:
            print("id wasn't found")

    def get_user_name(self, id):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT * from " + self.__tablename + ";"
        print(strsql)
        cursor = conn.execute(strsql)
        for row in cursor:
            if id == row[0]:
                return row[3]

    def insert_user(self, email, password, username):
        if not self.email_isexist(email):
            conn = sqlite3.connect('Super_List_Data_Base.db')
            insert_query = "INSERT INTO " + self.__tablename + " (" + self.__email + "," + self.__password + "," + \
             self.__username + ") VALUES"
            insert_query += "(" + "'" + email + "'" + "," + "'" + password + "'" + "," + "'" + username + "'" + ");"
            print(insert_query)
            conn.execute(insert_query)
            conn.commit()
            conn.close()
            print("Record created successfully")
        else:
            print("This email is already in the system")

    def select_user_by_email(self, email):
        if self.email_isexist(email):
            conn = sqlite3.connect('Super_List_Data_Base.db')
            print("Opened database successfully")
            strsql = "SELECT email, username, password  from " + self.__tablename + " where " + self.__email + "=" + \
                     "\'" + email + "\'"
            print(strsql)
            cursor = conn.execute(strsql)
            return cursor
        else:
            print("Email wasn't found")

    def email_isexist(self, email):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT email from " + self.__tablename + ";"
        print(strsql)
        cursor = conn.execute(strsql)
        for row in cursor:
            if email == row[0]:
                return True
        return False

    def user_isexist(self, email, password):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT * from " + self.__tablename + ";"
        print(strsql)
        cursor = conn.execute(strsql)
        for row in cursor:
            if email == row[1] and password == row[2]:
                return True
        return False



class Mylist:
    """Creates database with users table includes:
       create query
       insert query
       select query
    """

    def __init__(self, tablename="mylist", userid = "userid", product="product", locationnum ="locationnum", locationname ="locationname"):
        self.__tablename = tablename
        self.__userid = userid
        self.__product = product
        self.__locationnum = locationnum
        self.__locationname = locationname
        id = str(self.__userid)
        print("Opened database successfully")
        query_str = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + id + " INTEGER " + ","
        query_str += " " + self.__product + " TEXT ,"+ self.__locationname + " TEXT ," + self.__locationnum + " INTEGER    NOT NULL " + ","
        query_str += " " + " FOREIGN KEY ( userid ) REFERENCES users( userid ));"
        #"FOREIGN KEY(PersonID) REFERENCES Persons(PersonID)"
        conn = sqlite3.connect('Super_List_Data_Base.db')
        # conn.execute("drop table users")
        conn.execute(query_str)
        print("My list table created successfully")
        conn.commit()
        conn.close()


    def __str__(self):
        return "table  name is ", self.__tablename

    def print_table(self, product):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT * from " + self.__tablename + ";"
        print(strsql)
        cursor = conn.execute(strsql)
        for row in cursor:
            # if product == row[0]:
            print("product: " + row[0] + "\tlocation: " + str(row[1]))

    def get_table_name(self):
        return self.__tablename

    def insert_product(self, product, locationnum, locationname, id):
        if not self.product_isexist(product, id):
            conn = sqlite3.connect('Super_List_Data_Base.db')
            insert_query = "INSERT INTO " + self.__tablename + " (" + self.__userid + "," + self.__product + "," + self.__locationnum + "," + self.__locationname + ") VALUES"
            insert_query += "("+ "'" + str(id) + "'" + "," + "'" + str(product) + "'" + "," + "'" + str(locationnum) + "'" + "," + "'" + str(locationname) + "'" +");"
            print(insert_query)
            conn.execute(insert_query)
            conn.commit()
            conn.close()
            print("Record created successfully")
        else:
            print("This product is already in the List")

    def product_isexist(self, product, id):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT * from " + self.__tablename + ";"
        print(strsql)
        cursor = conn.execute(strsql)
        for row in cursor:
            if id == row[0] and product == row[1]:
                return True
        return False


    def creat_product(self,data, pname, pclass, pclassnum):
        product = {
            'pname': pname,
            'pclass': pclass,
            'pclassnum':pclassnum
        }
        data.append(product)
        return data

    def findmin(self, mylist):
        if len(mylist) == 0:
            return 0
        min = mylist[0]['pclassnum']
        for product in mylist:
            if min > product['pclassnum']:
                min = product['pclassnum']
        return min

    def delete_product(self, product, userid):
        if self.product_isexist(product, userid):
            print(product, " 123 " , userid)
            conn = sqlite3.connect('Super_List_Data_Base.db')
            insert_query = "DELETE FROM mylist WHERE userid={} AND product={};".format(userid, product)
            print(insert_query)
            conn.execute(insert_query)
            conn.commit()
            conn.close()
            print("Deleted successfully")
        else:
            print("This product wasn't in the List")

    def sortmylist(self, mylist):
        newlist = []
        for i in range(len(mylist)):
            for product in mylist:
                min = self.findmin(mylist)
                if min == product['pclassnum']:
                    addproduct = {
                    'pname': product['pname'],
                    'pclass': product['pclass']
                    }
                    newlist.append((addproduct))
                    mylist.remove(product)
        return newlist


    def get_my_products(self, id):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT * from " + self.__tablename + ";"
        print(strsql)
        cursor = conn.execute(strsql)
        mylist =[]
        for row in cursor:
            if row[0] == id:
                mylist = self.creat_product(mylist, row[1], row[2], row[3])
        mylist = self.sortmylist(mylist)
        return mylist



class Allproducts:
    """Creates database with users table includes:
       create query
       insert query
       select query
    """

    def __init__(self, tablename="allproducts", product="product", locationnum ="locationnum", locationname ="locationname"):
        self.__tablename = tablename
        self.__product = product
        self.__locationnum = locationnum
        self.__locationname = locationname
        print("Opened database successfully")
        query_str = "CREATE TABLE IF NOT EXISTS " + tablename + "("
        query_str += " " + self.__product + " TEXT ," + self.__locationname + " TEXT ," + self.__locationnum + " INTEGER    NOT NULL " + ");"
        #"FOREIGN KEY(PersonID) REFERENCES Persons(PersonID)"
        conn = sqlite3.connect('Super_List_Data_Base.db')
        # conn.execute("drop table users")
        conn.execute(query_str)
        print("All products table created successfully")
        conn.commit()
        conn.close()

    def get_table_name(self):
        return self.__tablename

    def creat_product(self,data, pname, pclass):
        product = {
            'pname': pname,
            'pclass': pclass,
        }
        data.append(product)
        return data

    def get_products(self, location):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT * from " + self.__tablename + ";"
        print(strsql)
        cursor = conn.execute(strsql)
        productlist = ["", "Fruits and Vegetables", "Drinks", "Meat, Chicken and Fish", "Bread", "Milk, Cheese and Eggs","Snacks"]
        list =[]
        print(location, "loc")
        if not location:
            print(1)
            for row in cursor:
                list = self.creat_product(list, row[0], row[1])
        elif location not in productlist:
            print(2)
            for row in cursor:
                if row[0] == location:
                    list = self.creat_product(list, row[0], row[1])
        else:
            print(3)
            for row in cursor:
                if row[1] == location:
                    list = self.creat_product(list, row[0], row[1])
        return list


    def insert_product(self, product, locationnum, locationname):
        if not self.product_isexist(product):
            conn = sqlite3.connect('Super_List_Data_Base.db')
            insert_query = "INSERT INTO " + self.__tablename + " (" + self.__product + "," + self.__locationnum + "," + self.__locationname + ") VALUES"
            insert_query += "(" + "'" + str(product) + "'" + "," + "'" + str(
                locationnum) + "'" + "," + "'" + str(locationname) + "'" + ");"
            print(insert_query)
            conn.execute(insert_query)
            conn.commit()
            conn.close()
            print("Record created successfully")
        else:
            print("This product is already in the List")

    def product_isexist(self, product):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT * from " + self.__tablename + ";"
        print(strsql)
        cursor = conn.execute(strsql)
        for row in cursor:
            if product == row[1]:
                return True
        return False

    def get_product_info(self, product):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT * from " + self.__tablename + ";"
        print(strsql)
        cursor = conn.execute(strsql)
        for row in cursor:
            if product == row[0]:
                return (row[0], row[1], row[2])
        return False