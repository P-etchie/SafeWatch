import requests
import json
from kivy.clock import Clock
from kivy_garden.mapview import MapView, MapMarker, MapLayer, MapSource
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.graphics import Color
from View.base_screen import BaseScreenView
from View import screens
from Model.map_screen import COUNTY_DATA


class ColoredMapMarker(MapMarker):
    def __init__(self, lat, lon, color, crime_count, **kwargs):
        super().__init__(lat=lat, lon=lon, **kwargs)
        self.color = color
        self.crime_count = crime_count
        self.update_marker_color()
        self.animate_marker()

    def update_marker_color(self):
        with self.canvas.before:
            Color(*self.color)

    def animate_marker(self):
        if self.crime_count >= 1000:
            anim = Animation(opacity=0.3, duration=0.8) + Animation(opacity=1, duration=0.8)
            anim.repeat = True
            anim.start(self)


class MapScreenView(BaseScreenView):
    prev = None
    _observers = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_double_tap = True
        self.markers = []
        self.zoom = 6
        self.lat, self.lon = 0.0236, 37.9062
        self.data = None
        self.view = None
        self.mapview = None

    @staticmethod
    def load_crime_data():
        with open('safewatch.json', "r", encoding="utf-8") as crime_json:
            data = json.load(crime_json)
            return data

    def on_enter(self):
        if self.app is None:
            self.app = MDApp.get_running_app()

        self.data = self.app.app_data
        self.mapview = self.ids.map_view
        self.mapview.background_color = (0.118, 0.118, 0.082, 1)

        self.add_county_markers()

    def switch_screen(self, scr, *args):
        screen_ = screens.screens.get(scr)
        if screen_:
            self.model = screen_['model']
            self.controller = screen_['controller'](self.model)
            self.view = self.controller.get_view()
            self.app.prev = self.app.manager_screens.current_screen.name
            self.app.manager_screens.current = self.view.name

    def add_county_markers(self, *args):
        for county in COUNTY_DATA:
            county_name = county["name"]
            latitude, longitude = county["lat"], county["lon"]

            crime_count = self.data['ReportedCrimes2023'].get(county_name, 0)

            if crime_count < 500:
                marker_color = (0, 1, 0, 1)  # Green (Safe)
            elif 500 <= crime_count < 1500:
                marker_color = (1, 1, 0, 1)  # Yellow (Moderate)
            else:
                marker_color = (1, 0, 0, 1)  # Red (Hot Crime Zone)

            marker = ColoredMapMarker(lat=latitude, lon=longitude, color=marker_color, crime_count=crime_count)
            marker.bind(on_release=lambda m, name=county_name: self.show_popup(name))
            self.mapview.add_widget(marker)

    def show_popup(self, county_name):
        crime_count = self.data['ReportedCrimes2023'].get(county_name, 0)
        last_year_count = self.data['ReportedCrimes2022'].get(county_name, 0)

        if crime_count > last_year_count:
            trend = "📈 Increasing"
        elif crime_count < last_year_count:
            trend = "📉 Decreasing"
        else:
            trend = "➖ Stable"

        if crime_count < 500:
            crime_status = "✅ Safe Zone"
            title_color = "#008000"
        elif 500 <= crime_count < 999:
            crime_status = "⚖️ Moderate Crime Zone"
            title_color = "#FFFF00"
        else:
            crime_status = "🔥 Hot Crime Zone"
            title_color = "#FF0000"

        popup_title = f"{county_name}  {crime_status} {trend}"

        county_info = {
            "2023": crime_count,
            "2022": last_year_count,
            "2021": self.data['ReportedCrimes2021'].get(county_name, "N/A"),
            "2020": self.data['ReportedCrimes2020'].get(county_name, "N/A"),
            "2019": self.data['ReportedCrimes2019'].get(county_name, "N/A"),
            "2018": self.data['ReportedCrimes2018'].get(county_name, "N/A"),
        }

        box_layout = MDBoxLayout(orientation='vertical', padding="10dp", spacing="10dp")

        for year, count in county_info.items():
            box_layout.add_widget(MDLabel(
                text=f"[color=#FFA500]Cases in {year}:[/color] [color=#008080]{count}[/color]",
                markup=True,
                bold=True,
                font_style="H6",
                halign="left"
            ))

        popup = Popup(
            title=popup_title,
            content=box_layout,
            size_hint=(0.5, 0.4),
            auto_dismiss=True,
            separator_color="teal",
            background_color='#1E1E15',
            opacity=0.95,
            pos_hint={"center_x": .7, "center_y": .7}
        )

        popup.open()
