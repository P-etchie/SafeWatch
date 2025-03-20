from View import screens
import json, kivy.logger
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from View.base_screen import BaseScreenView
from kivymd.uix.button  import MDFillRoundFlatIconButton


class TrendsScreenView(BaseScreenView):
    _observers = []
    user_reported_cases = str(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.data = None
        self.md_bg_color = "#1E1E15"

    def model_is_changed(self):
        self.model.notify_observers("trends screen")

    def on_enter(self, *args):
        if self.app is None:
            self.app = MDApp.get_running_app()
        self.user_reported_cases = self.app.user_reported_cases
        if self.data is None:
            self.data = self.app.app_data

        if not self.ids.crime_list.children:
            Clock.schedule_once(lambda dt: self.populate_crime_data(), 0.1)

    def switch_screen(self, scr, *args):
        screen_ = screens.screens.get(scr)
        if screen_:
            self.model = screen_['model']
            self.controller =  screen_['controller'](self.model)
            self.view = self.controller.get_view()
            self.app.prev = self.app.manager_screens.current_screen.name
            self.app.manager_screens.current = self.view.name
        else:
            kivy.logger.Logger.info(f"Got None As Screen")

    def populate_crime_data(self):
        try:
            counties_data = self.data["CountiesData"]
            reported_crimes = self.data["ReportedCrimes2023"]
            grid_layout = self.ids.crime_list
            if grid_layout.children:
                return

            for county, details in counties_data.items():
                total_crimes = reported_crimes.get(county, 0)

                card = MDCard(
                    orientation="vertical",
                    padding="10dp",
                    size_hint=(1, None),
                    height="400dp",
                    adaptive_height=True,
                    spacing="10dp",
                    on_release = lambda instance, c=county: self.county_card_details(c)
                )
                title_label = MDLabel(
                    text=county.upper(),
                    bold=True,
                    theme_text_color="Custom",
                    text_color=(0, 0.5, 1, 1),
                    halign="center",
                    size_hint_y=None,
                    height="30dp"
                )
                card.add_widget(title_label)

                crime_list = MDList()
                crimes = details.get("crimes", [])
                percentages = details.get("county_percent", [])

                for crime, percent in zip(crimes, percentages):
                    crime_count = int((percent / 100) * total_crimes)
                    crime_text = f"[b]{crime}:[/b] [color=#FF5722]{crime_count} cases[/color]"

                    crime_item = MDLabel(
                        text=crime_text,
                        markup=True,
                        theme_text_color="Primary",
                        halign="left",
                        size_hint_y=None,
                        height="30dp"
                    )
                    crime_list.add_widget(crime_item)

                card.add_widget(crime_list)
                grid_layout.add_widget(card)

        except Exception as e:
            print(f"Error loading crime data: {e}")

    def county_card_details(self, county):
        second_trend_screen = self.app.manager_screens.get_screen("secondtrend screen")
        second_trend_screen.county = county
        self.switch_screen("secondtrend screen")

    def filter_crime_data(self, county_name):

        for county in self.data['CountiesData'].keys():
            if county_name.lower() == county.lower() or county.lower() == county_name.lower():
                county_data = self.data['CountiesData'].get(county)
                reported_crimes = self.data["ReportedCrimes2023"]
                grid_layout = self.ids.crime_list
                total_crimes = reported_crimes.get(county, 0)

                card = MDCard(
                    orientation="vertical",
                    padding="10dp",
                    size_hint=(1, None),
                    height="400dp",
                    adaptive_height=True,
                    spacing="10dp",
                    on_release=lambda instance, c=county: self.county_card_details(c)
                )

                title_label = MDLabel(
                    text=county.upper(),
                    bold=True,
                    theme_text_color="Custom",
                    text_color=(0, 0.5, 1, 1),
                    halign="center",
                    size_hint_y=None,
                    height="30dp"
                )
                card.add_widget(title_label)
                crime_list = MDList()
                crimes = county_data.get("crimes", [])
                percentages = county_data.get("county_percent", [])

                for crime, percent in zip(crimes, percentages):
                    crime_count = int((percent / 100) * total_crimes)
                    crime_text = f"[b]{crime}:[/b] [color=#FF5722]{crime_count} cases[/color]"

                    crime_item = MDLabel(
                        text=crime_text,
                        markup=True,
                        theme_text_color="Primary",
                        halign="left",
                        size_hint_y=None,
                        height="30dp"
                    )
                    crime_list.add_widget(crime_item)
                card.add_widget(crime_list)
                if grid_layout.children:
                    grid_layout.clear_widgets()
                    grid_layout.add_widget(card)
                return

