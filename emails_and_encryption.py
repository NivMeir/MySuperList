import smtplib
import random
import bcrypt

class Extras:

    def __init__(self):
        self.__sender = "superlistcompany@gmail.com"
        self.__code_of_gmail = "sugermhziatllzeb"
        self.__smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        try:
            self.__smtpObj.starttls()
            self.__smtpObj.login(self.__sender, self.__code_of_gmail)
        except BaseException as e:
            print(e)

    def encrypt(self, text):
        dec = bcrypt.hashpw(text.encode(), bcrypt.gensalt())
        return dec.decode()

    def encryptiontest(self, old, new):
        return bcrypt.hashpw(new.encode(), old.encode()) == old.encode()

    def codegenerator(self):
        code = random.randint(100000, 999999)
        return str(code)


    def send_email(self, email, code):
        print('sending email...')
        sender = "superlistcompany@gmail.com"
        receiver = email
        message = """From: Super List <superlistcompany@gmail.com>\n\
To: {} \n\
Subject: Super List Code \n\

Please enter the following code to confirm your email: {}
""".format(email, code)
        try:
            self.__smtpObj.sendmail(sender, receiver, message)
            print("Successfully sent email")
        except BaseException as e:
            print(e)

        


