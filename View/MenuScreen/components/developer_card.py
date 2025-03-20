from kivy.properties import StringProperty
# from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog


class DeveloperCard(MDDialog):
    avatar = StringProperty("assets/images/avatar.jpg")
    name = StringProperty("Admin")
    contact = StringProperty("+6594 080 967")
    height = 400
    size_hint = (1, 0.5)


