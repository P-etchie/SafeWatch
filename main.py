import os

import kivy.logger

USE_HOT_RELOAD = os.getenv("HOT_RELOAD", "1") == "1"

if USE_HOT_RELOAD:
    from kivymd.tools.hotreload.app import MDApp
else:
    from kivymd.app import MDApp

import importlib, logging, time, threading, schedule
import View.screens, json
from PIL import ImageGrab
from kivy import Config
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore
from kivy.properties import BooleanProperty, StringProperty
from kivy.graphics import Fbo, ClearColor, ClearBuffers, Rectangle
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDFadeSlideTransition, MDSwapTransition
from Model.database import FirebaseConnection
from Utility.format_news import fetch_crime_news

logging.getLogger("matplotlib").setLevel(logging.WARNING)


class SafeWatch(MDApp):
    KV_DIRS = [os.path.join(os.getcwd(), "View")]
    manager_screens = MDScreenManager()
    md_bg_color = get_color_from_hex('#1E1E15')
    prev = app_data = None
    app_notifications = BooleanProperty(False)
    app_email_notifications = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fireb = None
        self.fbo = None
        self.version = 1.0
        self.title = "SafeWatch"
        self.icon = "assets/images/safe1.png"
        self.__active_user = {"user": None, "loginAt": None}
        self._user_settings = None
        self.__user_reported_cases = str(0)
        self.call_report_count = 0
        self.sms_report_count = 0

    def build_app(self) -> MDScreenManager:
        Window.fullscreen = "auto"
        #Window.position = "custom"
        #Window.top = 40
        #Window.left = 10
        #Window.size = (1080 / 2.5, 2340 / 3)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.material_style = "M3"

        if self.manager_screens is None:
            self.manager_screens = MDScreenManager(MDFadeSlideTransition())

        Window.bind(on_key_down=self.on_keyboard_down)
        importlib.reload(View.screens)
        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

        return self.manager_screens

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers) -> None:
        if "meta" in modifiers or "ctrl" in modifiers and text == "r":
            self.rebuild()

    def on_start(self):
        if not self.fireb:
            self.fireb = FirebaseConnection()
            self.__user_reported_cases = self.fireb.user_total_crime_reports(self.__active_user['user'])

        self.start_news_scheduler()

    def start_news_scheduler(self):
        def run_scheduler():
            schedule.every(24).hours.do(fetch_crime_news)
            while True:
                schedule.run_pending()
                time.sleep(60)

        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()

    def on_stop(self):
        self.fbo = None
        self.save_report_counts()

    def on_pause(self):
        if not self.fbo:
            self.fbo = Fbo(size=self.root_window.size)

        with self.fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()
            self.root_window.canvas.ask_update()
            self.fbo.add(Rectangle(size=self.root_window.size, texture=self.root_window.texture))
        return True

    def on_resume(self):
        if self.fbo:
            with self.root_window.canvas:
                Rectangle(texture=self.fbo.texture, size=self.root_window.size)

    def create_session(self):
        Cache.register("ActiveUser", limit=None, timeout=None)
        Cache.append("ActiveUser", None, self._active_user)

    @staticmethod
    def clear_cache():
        Cache.remove("ActiveUser", key=None)
        for files in os.listdir("cache"):
            if files:
                os.remove(os.path.join("cache", files))
            else:
                return

    def save_app_settings(self):
        if self._user_settings is None:
            self._user_settings = JsonStore("app_settings.json")
        self._user_settings.put('general', dark_mode=True)
        self._user_settings.put('general', language='en')
        self._user_settings.put('notifications', push_notifications=self.app_notifications)
        self._user_settings.put('notifications', email_notifications=self.app_email_notifications)

    def on_language_change(self):
        self.root.clear_widgets()
        self.root.add_widget(self.build_app())

    @property
    def active_user(self):
        return self.__active_user

    @active_user.setter
    def active_user(self, activeUser):
        self.__active_user = activeUser

    @property
    def user_reported_cases(self):
        return self.__user_reported_cases

    @user_reported_cases.setter
    def user_reported_cases(self, cases_reported):
        self.__user_reported_cases = str(cases_reported)

    @staticmethod
    def terminate_application():
        exit(0)

    def save_report_counts(self):
        try:
            settings_file = "app_settings.json"

            if os.path.exists(settings_file):
                with open(settings_file, "r") as file:
                    settings = json.load(file)
            else:
                settings = {"native_reports": {"call_reports": 0, "sms_reports": 0, "media_uploads": 0}}

            settings["native_reports"]["call_reports"] += self.call_report_count
            settings["native_reports"]["sms_reports"] += self.sms_report_count

            with open(settings_file, "w") as file:
                json.dump(settings, file, indent=4)

            kivy.logger.Logger.info(f"Update Report Count Success")

        except Exception as e:
            kivy.logger.Logger.info(f"Error saving report counts: {e}")

SafeWatch().run()
