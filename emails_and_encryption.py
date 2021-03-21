import smtplib
import random
import bcrypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
def codegenerator(name):
    code = ""
    num = 5
    for letter in name:
        if num != 0:
            if letter.isalpha():
                number = str(ord(letter) - 96)
                rand = str(random.choice(string.ascii_letters))
                rand = rand.lower()
                code += number + rand
                num -= 1
    print(code)

def send(email, code):
    code_of_gmail = "sugermhziatllzeb"
    smtpObj = smtplib.SMTP('smtp.gmail.com', 25)
    smtpObj.starttls()
    smtpObj.login("superlistcompany@gmail.com", code_of_gmail)
    multipart_msg = MIMEMultipart()
    message = "hi " + str(code)
    multipart_msg['From'] = email
    multipart_msg['To'] = email
    multipart_msg['Subject'] = "JournalDev Subject"
    multipart_msg.attach(MIMEText(message, 'plain'))
    smtpObj.send_message(multipart_msg)
    del multipart_msg
    smtpObj.quit()
    print("Successfully sent email")"""


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


#abc = Emails()
#abc.encrypt("hamagniv28")
#abc.checkpassdecreaption("$2b$12$GjzIy.zYxXJacHsfL/bo5OXVnUeovPiimHdVOuPenZv5hrKuNJLkW", "hamagniv28")
#send_email("nivmeir2804@gmail.com", 123456)
#codegenerator("m")
