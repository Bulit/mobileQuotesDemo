from datetime import datetime
import json, glob, random
from pathlib import Path
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

Builder.load_file('design.kv')

# root
class LoginScreen(Screen):
    def login(self, uname, pword):
        if uname and pword:
            with open("users.json") as file:
                users = json.load(file)
            if uname in users and users[uname]['password'] == pword:
                self.manager.transition.direction = "left"
                self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password"

    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        if uname and pword:
            with open("users.json") as file:
                users = json.load(file)
            if uname in users:
                self.ids.incorrect_input.text = "Username already exist"
            else:
                users[uname] = {'username': uname, 'password': pword, 
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                # overwrite json file with new data
                with open("users.json", 'w') as file:
                    json.dump(users, file)
                self.manager.current = "sign_up_screen_success"
        else:
            self.ids.incorrect_input.text = "Wrong username or password"

class SignUpScreenSuccess(Screen):
    def back_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, mood):
        mood = mood.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]

        if mood in available_feelings:
            with open(f"quotes/{mood}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try other feeling"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        Window.clearcolor = (46/255,81/255,95/255,1)
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()