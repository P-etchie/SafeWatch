from kivymd.uix.label import MDLabel
from View.base_screen import BaseScreenView
from View import screens
import kivy.logger, hashlib
from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar
from Model.database import FirebaseConnection


class SignupScreenView(BaseScreenView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.user_data = {
            "fullname": "",
            "username": "",
            "email": "",
            "passwd": "",
            "phone": "",
            "address": ""
        }

    def on_enter(self, *args):
        if not self.app:
            self.app = MDApp.get_running_app()

    def model_is_changed(self) -> None:
        self.model.notify_observers("signup screen")

    def registerUser(self, fullnameId, usernameId, emailId, pass_field1, pass_field2,
                     phoneId):
        if self.app.fireb is None:
            self.app.fireb = FirebaseConnection()

        if pass_field1.text != pass_field2.text:
            pass_field2.line_color_normal = '#FF474C'
            pass_field1.line_color_normal = '#FF474C'
            return MDSnackbar(MDLabel(text="Passwords not matching",
                                      text_color="#FF474C",
                                      theme_text_color="Custom")
                              ).open()

        elif len(pass_field1.text) != len(pass_field2.text):
            pass_field2.line_color_normal = '#FF474C'
            pass_field1.line_color_normal = '#FF474C'
            return MDSnackbar(MDLabel(text="Password length not matching",
                                      text_color="#FF474C",
                                      theme_text_color="Custom")
                              ).open()
        
        elif (len(pass_field1.text) < 8) and (len(pass_field2.text) < 8):
            pass_field2.line_color_normal = '#FF474C'
            pass_field1.line_color_normal = '#FF474C'
            return MDSnackbar(MDLabel(text="Password should be 8 characters long",
                                      text_color="#FF474C",
                                      theme_text_color="Custom")
                              ).open()
        
        elif usernameId.text is None:
            usernameId.line_color_normal = '#FF474C'
            return MDSnackbar(MDLabel(text="username field empty",
                                      text_color="#FF474C",
                                      theme_text_color="Custom")
                              ).open()

        passwd_hash = hashlib.sha512(bytes(pass_field2.text,"utf-8")).hexdigest()
        self.user_data.__setitem__("fullname", fullnameId.text)
        self.user_data.__setitem__("username", usernameId.text)
        self.user_data.__setitem__("email", emailId.text)
        self.user_data.__setitem__("phone", phoneId.text)
        self.user_data.__setitem__('passwd', passwd_hash)
        
        rc, status = self.app.fireb.register_new_user(self.user_data)
        
        if rc == 0:
            if status == "user-exists":
                return MDSnackbar(MDLabel(text="Username already taken",
                                   text_color="#FF474C",
                                   theme_text_color="Custom")
                           ).open()
            elif status == "user-field-empty":
                return MDSnackbar(MDLabel(text="Username field cannot be empty",
                                   text_color="#FF474C",
                                   theme_text_color="Custom")
                           ).open()
            else:
                return MDSnackbar(MDLabel(text=status,
                                   text_color="#FF474C",
                                   theme_text_color="Custom")
                           ).open()
        elif rc == 1 :
            self.switch_screen("login screen")
            return MDSnackbar(MDLabel(text="Registration Successful",
                                   text_color="teal",
                                   theme_text_color="Custom")
                           ).open()

    def switch_screen(self, scr, *args):
        screen_ = screens.screens.get(scr)
        if screen_:
            self.model = screen_['model']
            self.controller = screen_['controller'](self.model)
            self.view = self.controller.get_view()
            self.app.prev = self.app.manager_screens.current_screen.name
            self.app.manager_screens.current = self.view.name
        else:
            kivy.logger.Logger.info(f"{screen_}: Got None as screen")

    def on_leave(self, *args):
        if self.ids.pass_field2.text or self.ids.pass_field1.text:
            self.ids.pass_field2.text = self.ids.pass_field1.text = ""

        if self.ids.username.text or self.ids.email_address.text:
            self.ids.username.text = ""
            self.ids.email_address.text = ""

        if self.ids.fullname.text or self.ids.phone.text:
            self.ids.fullname.text = ""
            self.ids.phone.text = ""