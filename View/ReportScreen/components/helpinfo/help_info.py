from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.snackbar import MDSnackbar
from kivymd.app import MDApp
from kivy.properties import ListProperty, ObjectProperty
from plyer import filechooser
import os, pandas


class HelpInfo(MDBoxLayout, CommonElevationBehavior):
    reports = ListProperty([])
    report_screen = ObjectProperty(None)

    def __init__(self, report_screen, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.md_bg_color = "#1E1E15"
        self.report_screen = report_screen





