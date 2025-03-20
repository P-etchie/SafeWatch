# from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatIconButton

class UserCloudUpload(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.pos_hint = {"bottom": .3}
        #self.content_cls = MDLabel(text="Turn-On email notifications to see the pricing")
        self.buttons = [MDFillRoundFlatIconButton(icon='close',
                                                  icon_color= "red",
                                                  theme_icon_color="Custom",
                                                  text='CLOSE',
                                                  text_color="red",
                                                  theme_text_color="Custom",
                                                  md_bg_color="#3D4127",
                                                  on_release=lambda x: self.dismiss())]
        self.create_buttons()
        self.create_items()

