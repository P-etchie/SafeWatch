import datetime
from View.base_screen import BaseScreenView
from View import screens
from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.screenmanager import MDScreenManager
from Model.database import FirebaseConnection


class LoginScreenView(BaseScreenView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None
        self.app = None

    def model_is_changed(self) -> None:
        self.model.notify_observers('login screen')

    def on_enter(self, *args):
        if self.app is None:
            self.app = MDApp.get_running_app()
        if self.sm is None:
            self.sm = MDScreenManager()
        if self.app.fireb is None:
            self.app.fireb = FirebaseConnection()

    def switch_screen(self, scr, *args):
        screen_ = screens.screens.get(scr)
        if screen_:
            self.model = screen_['model']
            self.controller =  screen_['controller'](self.model)
            self.view = self.controller.get_view()
            self.app.prev = self.app.manager_screens.current_screen.name
            self.app.manager_screens.current = self.view.name

    def validate_login(self, user_field, pass_field):
        if not user_field.text and not pass_field.text:
            return MDSnackbar(MDLabel(text="Kindly fill both fields to login",
                               text_color="#FF474C",
                               halign="center",
                               theme_text_color="Custom")).open()
        else:
            rc, status = self.app.fireb.validate_user_login(user_field.text, pass_field.text)
            if rc == 0:
                if status == "user404":
                    MDSnackbar(MDLabel(text="User not found",
                                       text_color="red",
                                       theme_text_color="Custom")
                               ).open()
                elif status == "invalidPasswd":
                    return MDSnackbar(MDLabel(text="Invalid Password",
                                              text_color="red",
                                              theme_text_color="Custom")
                                      ).open()
                else:
                    return MDSnackbar(MDLabel(text=status,
                                              text_color="red",
                                              theme_text_color="Custom")
                                      ).open()
            elif rc == 1 and status == "success":
                self.app.active_user = {"user":user_field.text, "loginAt":datetime.datetime.now()}
                self.switch_screen("home screen")
                return MDSnackbar(MDLabel(text=f"Welcome Back {user_field.text}",
                                              text_color="teal",
                                              theme_text_color="Custom")
                                      ).open()

    def toggle_password(self, instance):
        if instance:
            instance.selection_color = instance.fill_color_focus
            is_hidden = instance.password
            fade_anim = Animation(opacity=0, duration=0.2) + Animation(opacity=1, duration=0.2)
            icon_anim = Animation(angle=180, duration=0.2) + Animation(angle=360, duration=0.2)
            instance.password = not is_hidden
            instance.icon_right = "eye-off" if is_hidden else "eye"
            fade_anim.start(instance)
        else:
            return

    def on_leave(self, *args):
        if self.ids.password.text  or self.ids.username.text:
            self.ids.password.text = ""
            self.ids.username.text = ""

