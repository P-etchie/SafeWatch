import kivy.logger
from View import screens
from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar
from View.base_screen import BaseScreenView
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from Model.login_screen import BaseScreenModel


class ProfileScreenView(BaseScreenView):
    phone = StringProperty('...')
    email = StringProperty('...')
    fullname = StringProperty('...')
    street_address = StringProperty('...')
    profile_image = StringProperty("assets/images/avatar.jpg")
    _observers = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.user_data = None
        self.dialog = None

    def on_enter(self, *args):
        if self.app is None:
            self.app = MDApp.get_running_app()
        if self.user_data is None:
            self.user_data = self.app.fireb.get_user_info(self.app.active_user['user'])
            self.set_user_details(self.user_data)

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

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

    def edit_profile(self):
        if not self.dialog:
            self.dialog = MDDialog(
                md_bg_color=self.app.md_bg_color,
                title="Edit Profile",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="fullname_field",
                        hint_text="Full Name",
                        text=self.fullname,
                    ),
                    MDTextField(
                        id="email_field",
                        hint_text="Email",
                        text=self.email,
                    ),
                    MDTextField(
                        id="phone_field",
                        hint_text="Phone",
                        text=self.phone,
                    ),
                    MDTextField(
                        id="address_field",
                        hint_text="Street Address",
                        text=self.street_address,
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="300dp",
                ),
                buttons=[
                    MDRaisedButton(
                        text="CANCEL",
                        on_release=lambda _: self.dialog.dismiss(),
                    ),
                    MDRaisedButton(
                        text="SAVE",
                        on_release=lambda _: self.save_profile_changes(),
                    ),
                ],
            )
        self.dialog.open()

    def save_profile_changes(self):
        if not self.dialog:
            return

        updated_data = {
            "fullname": self.dialog.content_cls.ids.fullname_field.text.strip(),
            "email": self.dialog.content_cls.ids.email_field.text.strip(),
            "phone": self.dialog.content_cls.ids.phone_field.text.strip(),
            "address": self.dialog.content_cls.ids.address_field.text.strip()
        }

        user_id = self.app.active_user["user"]

        try:
            self.app.fireb.db.collection("Users").document(user_id).update(updated_data)

            self.fullname = updated_data["fullname"]
            self.email = updated_data["email"]
            self.phone = updated_data["phone"]
            self.street_address = updated_data["address"]

            self.dialog.dismiss()

            return MDSnackbar(MDLabel(text="Profile Information Updated Successfully ",
                              text_color="teal",
                              theme_text_color="Custom")
                              ).open()


        except Exception as e:
            return MDSnackbar(MDLabel(text=f"{e}",
                                      text_color="red",
                                      theme_text_color="Custom")
                              ).open()

    def logout(self):
        self.switch_screen("login screen")
        self.app.active_user.clear()
        # print(self.app.active_user)

    def set_user_details(self, user_data):
        self.phone = user_data.get('phone')
        self.email = user_data.get('email')
        self.fullname = user_data.get('fullname')
        self.street_address = user_data['address']
