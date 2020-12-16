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
        print(query_str)
        conn.execute(query_str)
        print("Table created successfully")
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


    def get_user_email(self):
        return self.__email

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

    def __init__(self, tablename="mylist", userid = "userid", product="product", location ="location"):
        self.__tablename = tablename
        self.__userid = userid
        self.__product = product
        self.__location = location
        id = str(self.__userid)
        print("Opened database successfully")
        query_str = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + id + " INTEGER " + ","
        query_str += " " + self.__product + " TEXT ," + self.__location + " INTEGER    NOT NULL " + ","
        query_str += " " + " FOREIGN KEY ( userid ) REFERENCES users( userid ));"
        #"FOREIGN KEY(PersonID) REFERENCES Persons(PersonID)"
        conn = sqlite3.connect('Super_List_Data_Base.db')
        # conn.execute("drop table users")
        conn.execute(query_str)
        print("Table created successfully")
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

    def insert_producet(self, product, location, id):
        if not self.product_isexist(product, id):
            conn = sqlite3.connect('Super_List_Data_Base.db')
            insert_query = "INSERT INTO " + self.__tablename + " (" + self.__userid + "," + self.__product + "," + self.__location + ") VALUES"
            insert_query += "("+ "'" + str(id) + "'" + "," + "'" + product + "'" + "," + "'" + str(location) + "'" + ");"
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



