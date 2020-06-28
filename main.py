# from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import  ObjectProperty
from kivy.uix.popup import  Popup
from Signin.db import DataBase

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

class MainWindow(Screen):

    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created

class SignInWindow(Screen):
    email=ObjectProperty(None)
    password=ObjectProperty(None)

    def login_btn(self):

        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def create_account_btn(self):
        self.reset()
        sm.current = "signup"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class SignUpWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit_btn(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""

    def already_have_account_btn(self):
        self.reset()
        sm.current = "login"

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('my.kv')
sm = WindowManager()
db = DataBase("users.txt")

def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()

screens = [SignInWindow(name="login"), SignUpWindow(name="signup"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"

class MYApp(MDApp):
    def __init__(self,**kwargs):
        self.title = "Login App"
        self.icon = "1.ico"
        super().__init__(**kwargs)

    def build(self):
        return sm

if __name__ == '__main__':
    MYApp().run()