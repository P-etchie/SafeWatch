import kivy.logger
from kivy.clock import Clock
from View import screens
from View.base_screen import BaseScreenView
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatIconButton, MDIconButton

class ResetScreenView(BaseScreenView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.view = None
        self.app = None

    def on_enter(self):
        if not self.app:
            self.app = MDApp.get_running_app()

    def switch_screen(self, scr, *args):
        screen_ = screens.screens.get(scr)
        if screen_:
            self.model = screen_['model']
            self.controller = screen_['controller'](self.model)
            self.view = self.controller.get_view()
            self.app.prev = self.app.manager_screens.current_screen.name
            self.app.manager_screens.current = self.view.name
        else:
            kivy.logger.Logger.info(f"{scr} : Got None As Screen ")

    def send_reset_link(self, username, pass_field1, pass_field2):
        if pass_field1.text and pass_field2.text and username.text:

            if len(pass_field1.text) != len(pass_field2.text):
                MDSnackbar(MDLabel(text="Passwords length not matching",
                                   font_size="12sp",
                                   text_color="#FF474C",
                                   theme_text_color="Custom", ),
                           duration=0.8).open()

            elif len(pass_field2.text) < 8 and len(pass_field1.text) < 8:
                MDSnackbar(MDLabel(text="Passwords must be 8 characters long",
                                   font_size="12sp",
                                   text_color="#FF474C",
                                   theme_text_color="Custom", ),
                           duration=1).open()

            elif pass_field1.text != pass_field2.text:
                MDSnackbar(MDLabel(text="Passwords not matching",
                                   font_size="12sp",
                                   text_color="#FF474C",
                                   theme_text_color="Custom", ),
                           duration=0.8
                           ).open()

            check_user = self.app.fireb.get_user_info(username.text)

            if check_user != "user404":
                rc, status = self.app.fireb.update_user_password(username.text, pass_field1.text)
                if rc == 1 and status == "success":
                    self.show_success_dialog()
                else:
                    self.show_error_dialog(status)
            else:
                return self.show_error_dialog(f"User with username {username.text} Not Found")

        else:
            MDSnackbar(MDLabel(text="All fields are required",
                               font_size="12sp",
                               text_color="#FF474C",
                               theme_text_color="Custom", ),
                       duration=0.8
                       ).open()

    def show_success_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Password Reset Success",
                text="You can now login with your new password",
                #text_color="green",
                buttons=[
                    MDIconButton(icon="close-box",
                                 icon_color="#FF474C",
                                 md_bg_color=self.app.md_bg_color,
                                 theme_icon_color="Custom",
                                 on_release=lambda x: self.dialog.dismiss())
                ]
            )
        self.dialog.open()

    def show_error_dialog(self, error_msg):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Error",
                text=error_msg,
                buttons=[
                    MDRaisedButton(text="Try Again", on_release=lambda x: self.dialog.dismiss())
                ]
            )
        self.dialog.open()

    def model_is_changed(self) -> None:
        self.model.notify_observers("home screen")

    def on_leave(self, *args):
        if self.ids.pass_field1.text or self.ids.pass_field2.text or self.ids.username.text:
            self.ids.pass_field1.text = ""
            self.ids.pass_field2.text = ""
            self.ids.usernme.text = ""


