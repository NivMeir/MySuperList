import sqlite3
import emails_and_encryption
passcheck = emails_and_encryption.Extras()

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


    def get_user_email(self, id):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT * from " + self.__tablename + ";"
        print(strsql)
        cursor = conn.execute(strsql)
        for row in cursor:
            if id == row[0]:
                return row[1]


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
            if email == row[1] and passcheck.encryptiontest(row[2], password):
                return True
        return False

    def update_password(self, email, newpass):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql ="UPDATE " + self.__tablename + " SET password= " + "'" + str(newpass) + "'" + " WHERE email= '" + email + "';"
        #UPDATE users SET password= 'hamagniv28' WHERE email= 'nivmeir2804@gmail.com';
        print(strsql)
        conn.execute(strsql)
        conn.commit()
        conn.close()
        print("password changed")


class Mylist:
    """Creates database with users table includes:
       create query
       insert query
       select query
    """

    def __init__(self, tablename="mylist", userid = "userid", product="product", locationnum ="locationnum", locationname ="locationname", shelf = "shelf"):
        self.__tablename = tablename
        self.__userid = userid
        self.__product = product
        self.__locationnum = locationnum
        self.__locationname = locationname
        self.__shelf = shelf
        id = str(self.__userid)
        print("Opened database successfully")
        query_str = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + id + " INTEGER " + ","
        query_str += " " + self.__product + " TEXT ,"+ self.__locationname + " TEXT ," + self.__locationnum + " INTEGER    NOT NULL " + "," + self.__shelf + " TEXT ,"
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

    def print_table(self):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT * from " + self.__tablename + ";"
        print(strsql)
        cursor = conn.execute(strsql)
        for row in cursor:
            # if product == row[0]:
            print("product: " + row[1] + "\tdepartment: " + str(row[2]) + "\tshelf: " + str(row[4]))

    def get_table_name(self):
        return self.__tablename

    def insert_product(self, product, locationnum, locationname, shelf, id):
        print(product, locationnum, locationname, shelf, id)
        if not self.product_isexist(product, id):
            conn = sqlite3.connect('Super_List_Data_Base.db')
            insert_query = "INSERT INTO " + self.__tablename + " (" + self.__userid + "," + self.__product + "," + self.__locationnum + "," + self.__locationname + "," + self.__shelf +") VALUES"
            insert_query += "("+ "'" + str(id) + "'" + "," + "'" + str(product) + "'" + "," + "'" + str(locationnum) +\
                            "'" + "," + "'" + str(locationname) + "'" + "," + "'" + str(shelf) + "'" +");"
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


    def creat_product(self,data, pname, pclass, pclassnum, shelf):
        product = {
            'pname': pname,
            'pclass': pclass,
            'pclassnum':pclassnum,
            'shelf':shelf
        }
        data.append(product)
        return data

    def delete_product(self, product, userid):
        if self.product_isexist(product, userid):
            conn = sqlite3.connect('Super_List_Data_Base.db')
            insert_query = "DELETE FROM mylist WHERE userid == {} AND product == '{}';".format(userid, product)
            print(insert_query)
            conn.execute(insert_query)
            conn.commit()
            conn.close()
            print("Deleted successfully")
        else:
            print("This product wasn't in the List")

    def get_my_products(self, id):
            """SELECT
    	userid,
    	product,
    	locationname,
    	locationnum,
    	shelf
    FROM
    	mylist
    ORDER BY
    	locationnum ASC,
    	shelf ASC;"""
            conn = sqlite3.connect('Super_List_Data_Base.db')
            insert_query = "SELECT userid, product, locationname, locationnum,shelf FROM mylist ORDER BY userid ASC, locationnum ASC, shelf ASC;"
            print(insert_query)
            cursor = conn.execute(insert_query)
            newlist = []
            for row in cursor:
                if row[0] == id:
                    addproduct = {
                        'pname': row[1],
                        'pclass': row[2],
                        'shelf': row[4]}
                    newlist.append(addproduct)
            print("done sorting")
            return newlist

"""
    def findminclass(self, mylist):
        if len(mylist) == 0:
            return 0
        min = mylist[0]['pclassnum']
        for product in mylist:
            if min > product['pclassnum']:
                min = product['pclassnum']
        return min

    def findminshelf(self, mylist, cmin):
        if len(mylist) == 0:
            return 0
        j=0
        for i in range(len(mylist)):
            if mylist[i]['pclassnum'] == cmin:
                j=i
        min = mylist[j]['shelf']
        for product in mylist:
            if cmin == product['pclassnum'] and  min > product['shelf']:
                min = product['shelf']
        return min

    def numofshelves(self, mylist, cmin):
        num = 0
        added = []
        for product in mylist:
            if product['pclassnum'] == cmin and product['shelf'] not in added:
                added.append(product['shelf'])
                num += 1
        return num

    def numofclasses(self, mylist):
        num = 0
        added = []
        for product in mylist:
            if product['pclassnum'] not in added:
                added.append(product['pclassnum'])
                num += 1
        return num

    def sortmylist(self, mylist):
        newlist = []
        numclasses = self.numofclasses(mylist)
        print("numclasses ", numclasses)
        for i in range(numclasses):
            print("i ", i)
            cmin = self.findminclass(mylist)
            print("cmin ", cmin)
            numshelves = self.numofshelves(mylist, cmin)
            print("numshelves ", numshelves)
            for j in range(numshelves):
                print("j ", j)
                smin = self.findminshelf(mylist, cmin)
                print("smin ", smin)
                for product in mylist:
                    print(product['pname'], product['pclassnum'], product['shelf'])
                    if cmin == product['pclassnum'] and smin == product['shelf']:
                        addproduct = {
                            'pname': product['pname'],
                            'pclass': product['pclass'],
                            'shelf': product['shelf']}
                        newlist.append(addproduct)
                        mylist.remove(product)
        print("done sorting")
        return newlist
"""



class Allproducts:
    """Creates database with users table includes:
       create query
       insert query
       select query
    """

    def __init__(self, tablename="allproducts", product="product", locationnum ="locationnum", locationname ="locationname", shelf = "shelf"):
        self.__tablename = tablename
        self.__product = product
        self.__locationnum = locationnum
        self.__locationname = locationname
        self.__shelf = shelf
        print("Opened database successfully")
        query_str = "CREATE TABLE IF NOT EXISTS " + tablename + "("
        query_str += " " + self.__product + " TEXT ," + self.__locationname + " TEXT ," + self.__locationnum + \
                     " INTEGER    NOT NULL ," + self.__shelf + " TEXT "+ ");"
        #"FOREIGN KEY(PersonID) REFERENCES Persons(PersonID)"
        conn = sqlite3.connect('Super_List_Data_Base.db')
        # conn.execute("drop table users")
        conn.execute(query_str)
        print("All products table created successfully")
        conn.commit()
        conn.close()

    def get_table_name(self):
        return self.__tablename

    def creat_product(self,data, pname, pclass, shelf):
        product = {
            'pname': pname,
            'pclass': pclass,
            'shelf': shelf
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
        if not location:
            for row in cursor:
                list = self.creat_product(list, row[0], row[1], row[3])
        elif location not in productlist:
            for row in cursor:
                if row[0] == location:
                    list = self.creat_product(list, row[0], row[1], row[3])
        else:
            for row in cursor:
                if row[1] == location:
                    list = self.creat_product(list, row[0], row[1], row[3])
        return list


    def insert_product(self, product, shelf, locationnum, locationname):
        if not self.product_isexist(product):
            conn = sqlite3.connect('Super_List_Data_Base.db')
            insert_query = "INSERT INTO " + self.__tablename + " (" + self.__product + "," + self.__locationnum + "," + self.__locationname + "," + self.__shelf + ") VALUES"
            insert_query += "(" + "'" + str(product) + "'" + "," + "'" + str(
                locationnum) + "'" + "," + "'" + str(locationname) + "'" + "," + "'" + str(shelf) + "'" + ");"
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
                return (row[0], row[1], row[2], row[3])
        return False

    def isempty(self):
        conn = sqlite3.connect('Super_List_Data_Base.db')
        strsql = "SELECT * from " + self.__tablename + ";"
        print(strsql)
        lines = 0
        cursor = conn.execute(strsql)
        for row in cursor:
            lines += 1
        return lines == 0
