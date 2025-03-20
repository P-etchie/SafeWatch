import kivy.logger
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.fitimage import FitImage
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from View.base_screen import BaseScreenView
from View.MenuScreen.components.developer_card import DeveloperCard
from View import screens


class MenuScreenView(BaseScreenView):
    _observers = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.app = None
        self.__dev_info__ = {"developer_name": "Patience Waweru",
                             "contact": "+657 9408 0967",
                             "email": "admin@safewatch.org"}

    def on_enter(self, *args):
        if self.app is None:
            self.app = MDApp.get_running_app()


    def model_is_changed(self) -> None:
        self.model.notify_observers("menu screen")
        
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


    def show_about(self):
        if not self.dialog:
            content = MDBoxLayout(
                orientation="vertical",
                spacing="30dp",
                size_hint_y= 0.6,
                adaptive_height=True,
            )
            avatar = FitImage(
                source="assets/images/avatar.jpg",
                size_hint= (None,None),
                size=( dp(100),dp(100) ),
                radius=[50,],
                pos_hint={"center_x": 0.5}
            )
            name_label = MDLabel(
                text=f"[b][color=#FF5722]Developer:[/b][/color] {self.__dev_info__.get('developer_name')}",
                theme_text_color="Primary",
                # font_size="",
                halign="center",
                markup=True,
            )

            contact_label = MDLabel(
                text=f"[b][color=#FF5722]Contact:[/b][/color] {self.__dev_info__.get('contact')}",
                theme_text_color="Primary",
                # font_style="H6",
                halign="center",
                markup=True
            )
            email_label = MDLabel(
                text=f"[b][color=#FF5722]Email:[/b][/color] {self.__dev_info__.get('email')}",
                theme_text_color="Primary",
                # font_style="H6",
                halign="center",
                markup=True
            )

            content.add_widget(avatar)
            content.add_widget(name_label)
            content.add_widget(contact_label)
            content.add_widget(email_label)

            self.dialog = MDDialog(
                title="Know The Developer",
                type="custom",
                content_cls=content,
                md_bg_color=self.app.md_bg_color,
                buttons=[
                    MDIconButton(
                        icon="close-box",
                        icon_color="#FF474C",
                        md_bg_color=self.app.md_bg_color,
                        theme_icon_color="Custom",
                        theme_text_color="Custom",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
                size_hint_y=.6,
                size_hint_x=.8
            )
        self.dialog.open()

    def toggle_notifications(self, instance):
        if not self.app.app_notifications:
            self.app.app_notifications = BooleanProperty(True)
            if instance.text:
                instance.text = "Disable Push Notifications"
            MDSnackbar(MDLabel(text="Push Notifications Enabled",
                               theme_text_color="Custom",
                               text_color="teal"),
                        duration=1).open()
        else:
            self.app.app_notifications = BooleanProperty(False)
            if instance.text:
                instance.text = "Enable Push Notifications"
            MDSnackbar(MDLabel(text="Push Notifications Disabled",
                               theme_text_color="Custom",
                               text_color="teal"),
                       duration=1).open()

    def toggle_email_alerts(self, instance):
        if not self.app.app_email_notifications:
            self.app.app_email_notifications = BooleanProperty(True)
            if instance.text:
                instance.text = "Disable Email Alerts"
            MDSnackbar(MDLabel(text="Email Notifications Enabled",
                               theme_text_color="Custom",
                               text_color="teal"),
                               duration=1).open()
            # instance.ids.email_icon.icon_left_color = "teal"
            print(instance.ids)
        else:
            self.app.app_email_notifications = BooleanProperty(False)
            if instance.text:
                instance.text = "Enable Email Alerts"
            MDSnackbar(MDLabel(text="Email Notifications Disabled",
                               theme_text_color="Custom",
                               text_color="teal"),
                               duration=1).open()

    def toggle_theme(self):
        if self.app.theme_cls.theme_style == "Dark":
            self.app.theme_cls.theme_style = "Light"
            self.app.md_bg_color = 'white'
            self.md_bg_color = self.app.md_bg_color
            self.theme_cls.primary_palette = "BlueGray"
        else:
            self.app.theme_cls.theme_style = "Dark"



        
