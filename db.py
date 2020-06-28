import datetime
import time
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import pyrebase
from getpass import getpass

firebaseConfig = {
    "apiKey": "AIzaSyB_eHoSmqAxsGnLYpOT9g_1Uh4xz6mJJPo",
    "authDomain": "loginpage-980d8.firebaseapp.com",
    "databaseURL": "https://loginpage-980d8.firebaseio.com",
    "projectId": "loginpage-980d8",
    "storageBucket": "loginpage-980d8.appspot.com",
    "messagingSenderId": "315170475265",
    "appId": "1:315170475265:web:4bbdd605ffbe39e8159f00",
    "measurementId": "G-59H78G717C"
}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

class DataBase:
    def __init__(self,filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}
        for line in self.file:
            email, password, name, created = line.strip().split(";")
            self.users[email] = (password, name, created)
        self.file.close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            auth.create_user_with_email_and_password(email.strip(), password.strip())
            self.save()
            return 1
        else:
            self.invalidEmail()
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")

    def invalidEmail(self):
        pop = Popup(title='Error',
                    content=Label(text='Email already exists'),
                    size_hint=(None, None), size=(400, 400))

        pop.open()

    @staticmethod
    def get_date():
        # return str(datetime.datetime.now()).split(" ")[0]
        return str(time.strftime('%c'))





