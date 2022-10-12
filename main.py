from datetime import datetime
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

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

    def enlighten(self, mood):
        pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()