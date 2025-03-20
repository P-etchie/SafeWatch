from View import screens
from View.base_screen import BaseScreenView
import kivy.logger
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.screenmanager import MDScreenManager
from Utility.format_news import load_news


class HomeScreenView(BaseScreenView):
    _observers = []
    fit_mode = ObjectProperty("contain")
    welcome_text = StringProperty("Welcome Back")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.view = None
        self.active_user = None
        self.current_case_index = 0
        self.cases = None

    def on_enter(self, *args):
        if self.cases is None:
            self.cases = load_news()

        if self.app is None:
            self.app = MDApp.get_running_app()
        self.app.fireb.listen_for_new_cases(self.app.active_user['user'])
        self.app.user_reported_cases = self.app.fireb.user_total_crime_reports(self.app.active_user['user'])

        if self.active_user is None:
            self.active_user = 'admin'
        self.animate_case(self.ids.welcome)

        if self.app.theme_cls.theme_style == "Light":
            self.md_bg_color = "white"
        self.md_bg_color = self.app.md_bg_color

        if self.ids.report_list.children:
            self.add_report()

    def open_nav_drawer(self):
        self.app.root.ids.nav_drawer.set_state("open")

    def switch_screen(self, scr, *args):
        screen_ = screens.screens.get(scr)
        if screen_:
            self.model = screen_['model']
            self.controller = screen_['controller'](self.model)
            self.view = self.controller.get_view()
            self.app.prev = self.app.manager_screens.current_screen.name
            self.app.manager_screens.current = self.view.name
        else:
            kivy.logger.Logger.info(f"Got None As Screen")

    def model_is_changed(self) -> None:
        self.model.notify_observers("home screen")

    def add_report(self):
        rc, all_reports = self.app.fireb.get_all_reports()
        if rc == 1:
            self.ids.report_list.clear_widgets()
            for user_index, reports in all_reports.items():
                for report_index, report in reports.items():
                    crime_category = report.get("Category", "Unknown Category")
                    crime_type = report.get("Offence", "Unknown Crime")
                    location = report.get("Location", "Unknown Location")
                    time_occurred = report.get("TimeOccurred", "Unknown Time")

                    self.ids.report_list.add_widget(
                        ThreeLineListItem(
                            text=f"{crime_category}",
                            secondary_text=f"[{location}] {crime_type}",
                            tertiary_text=f"Reported: {time_occurred}"
                        )
                    )
        else:
            kivy.logger.Logger.info(all_reports)

    def animate_case(self, instance):
        if not self.cases or not isinstance(self.cases, list):
            instance.text = "No recent crime news available."
            return

        headlines = [news["headline"] for news in self.cases if "headline" in news]

        if not headlines:
            instance.text = "No crime-related news available."
            return

        instance.text = headlines[self.current_case_index]  # Set current headline
        instance.opacity = 0
        instance.x = -instance.width

        anim_in = Animation(x=5, opacity=1, duration=2.5, t='out_quad')
        anim_hold = Animation(duration=2.0)
        anim_out = Animation(x=self.width, opacity=0, duration=2.5, t='in_quad')

        anim = anim_in + anim_hold + anim_out
        anim.bind(on_complete=lambda *args: self.next_case(instance, headlines))
        anim.start(instance)

    def next_case(self, instance, headlines):
        self.current_case_index = (self.current_case_index + 1) % len(headlines)
        Clock.schedule_once(lambda dt: self.animate_case(instance), 0.5)

