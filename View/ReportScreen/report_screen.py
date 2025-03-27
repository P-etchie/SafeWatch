import collections
import os ,pandas
from datetime import datetime
import kivy.logger, json
from plyer import filechooser, gps
from functools import partial
from kivy.properties import StringProperty
from View import screens
from View.base_screen import BaseScreenView
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDRectangleFlatIconButton
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivy.utils import get_color_from_hex
from libs.device import MobileFeatures
from View.ReportScreen.components import UserCloudUpload, HelpInfo


class ReportScreenView(BaseScreenView):
    location=None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None
        self.app = None
        self.prev = None
        self.view = None
        self.selected = None
        self.chip_data = None
        self.info_dialog = None
        self.report_file = None
        self.user_custom_sms = StringProperty("")
        self.mobile_features = MobileFeatures()

    def on_enter(self, *args):
        if self.app is None:
            self.app = MDApp.get_running_app()
        if self.sm is None:
            self.sm = MDScreenManager()
        self.refresh_user_reports_on_change()

    def model_is_changed(self) -> None:
        self.model.notify_observers('report screen')

    def switch_to_prev_screen(self, *args):
        previous_screen = screens.screens.get(self.app.prev)
        if previous_screen:
            self.model = previous_screen['model']
            self.controller = previous_screen['controller'](self.model)
            self.view = self.controller.get_view()
            self.app.prev = self.app.manager_screens.current_screen.name
            self.app.manager_screens.current = self.view.name

    def switch_screen(self, scr, *args):
        screen_ = screens.screens.get(scr)
        if screen_:
            self.model = screen_['model']
            self.controller = screen_['controller'](self.model)
            self.view = self.controller.get_view()
            self.app.prev = self.app.manager_screens.current_screen.name
            self.app.manager_screens.current = self.view.name

    def share_chip(self, chipText, chipId):
        if chipId == self.selected:
            if hasattr(chipId, 'md_bg_color'):
                chipId.md_bg_color = get_color_from_hex("#2a3127")
            self.selected  = None
            self.chip_data = None

        else:
            if self.selected is None:
                if chipId and chipText:
                    if self.chip_data is None:
                        self.chip_data = chipText
                        if hasattr(chipId, 'md_bg_color'):
                            chipId.md_bg_color = get_color_from_hex('#008080')
                        self.selected = chipId
            else:
                MDSnackbar(
                    MDLabel(
                        text="Select Only One Category",
                        theme_text_color="Custom",
                        text_color="teal"
                    ),
                    duration=1,
                    snackbar_animation_dir="Left"
                    ).open()

    def show_info_dialog(self):
        if not self.info_dialog:
            content_box = HelpInfo(report_screen=self)
            self.info_dialog = MDDialog(
                title="Export Crime Reports",
                type="custom",
                content_cls=content_box,
                size_hint_y=0.5,
                padding="10dp",
                pos_hint={"top": 0.9},
                scale_y=0.5,
                md_bg_color='#1E1E15',
                buttons=[
                    MDIconButton(
                        icon="close-outline",
                        md_bg_color='#FF474C',
                        on_release=lambda x: self.info_dialog.dismiss()
                    )
                ]
            )
        self.info_dialog.open()

    def upload_user_local_crime_file(self):
        filechooser.open_file(on_selection=self.validate_and_upload_crime_file)

    def validate_and_upload_crime_file(self, selection):
        if not selection:
            MDSnackbar(MDLabel(text="No file selected!",
                               theme_text_color="Custom",
                               text_color="red")
                       ).open()
            return
        file_path = selection[0]
        print(file_path)
        return UserCloudUpload().open()

    def show_message_dialog(self):
        if not hasattr(self, 'message_dialog') or self.message_dialog is None:
            self.message_input = MDTextField(
                id="sms_report",
                hint_text="Enter message",
                multiline=True,
                mode="fill",
            )
            self.message_dialog = MDDialog(
                title="Send Crime SMS Report ",
                type="custom",
                content_cls=self.message_input,
                md_bg_color=self.md_bg_color,
                buttons=[
                    MDRectangleFlatIconButton(
                        icon='share',
                        text="Send",
                        #text_color="#D4DE95",
                        #md_bg_color="#3D4127",
                        theme_text_color="Custom",
                        on_release=lambda x: self.call_report_sms(self.message_input.text)
                    ),
                    MDRaisedButton(
                        text="Close",
                        text_color="#D4DE95",
                        md_bg_color='#FF474C',
                        theme_text_color="Custom",
                        on_release=lambda x: self.message_dialog.dismiss()
                    )
                ]
            )
        self.message_dialog.open()

    def call_report_sms(self, instance_text):
        if self.mobile_features.SendCrimeReportSms(instance_text):
            self.app.sms_report_count += 1
            return  MDSnackbar(MDLabel(text=f"SMS Report Sent Successfully",
                               text_color="teal",
                               theme_text_color="Custom")
                       ).open()
        else:
            return MDSnackbar(MDLabel(text=f"Technical error while processing sms",
                               text_color="red",
                               theme_text_color="Custom")
                       ).open()

    def show_call_dialog(self):
        if not hasattr(self, "call_dialog") or self.call_dialog is None:
            self.phone_input = MDTextField(
                id="phone_input",
                #hint_text="0800 722 203",
                text="0800 722 203",
                # text_color="teal",
                halign="left",
                line_color_normal=self.md_bg_color,
                input_type="number",
                mode = "rectangle",
                disabled=True,
            )
            self.call_dialog = MDDialog(
                title="Call Emergency Number",
                type="custom",
                content_cls=self.phone_input,
                md_bg_color=self.md_bg_color,
                buttons=[
                    MDRectangleFlatIconButton(
                        icon="call-made",
                        text="Call",
                        on_release=lambda x: self.call_emergency_number(self.phone_input.text)
                    ),
                    MDRaisedButton(
                        text="Close",
                        text_color='#D4DE95',
                        md_bg_color="#FF474C",
                        theme_text_color="Custom",
                        on_release=lambda x: self.call_dialog.dismiss()
                    )
                ]
            )
        self.call_dialog.open()

    def call_emergency_number(self, phone_number):
        if phone_number:
            kivy.logger.Logger.info(f"Calling {phone_number}...")
            self.app.call_report_count += 1
            self.call_dialog.dismiss()
        else:
            MDSnackbar(
                MDLabel(text="Enter a valid phone number!", theme_text_color="Custom", text_color="red"),
                duration=2
            ).open()

    def get_current_location(self, instance):
        if self.location is None:
            try:
                self.location = self.mobile_features.get_location()
                if self.location:
                    instance.text = self.location
                else:
                    self.location = self.mobile_features.get_geoip_location()
                    print(self.location)
                    instance.text = f"{self.location['city']}, {self.location['country']}"
            except Exception as exc:
                kivy.logger.Logger.info(exc)

    def show_datetime_picker(self):
        def on_date_set(instance, date_obj, date_range=None):  # Fix: Accept extra argument
            self.selected_date = date_obj
            time_picker = MDTimePicker()
            time_picker.bind(time=on_time_set)
            time_picker.open()

        def on_time_set(instance, time_obj):
            self.ids.time_button.text = f"{self.selected_date} {time_obj.strftime('%H:%M')}"

        date_picker = MDDatePicker()
        date_picker.bind(on_save=on_date_set)  # Fix: Correct event binding
        date_picker.open()

    def refresh_user_reports_on_change(self):
        reports = self.app.fireb.get_user_reports(self.app.active_user['user'])
        total_user_reports = len(reports.keys())
        self.ids.user_media_reports = str(0)
        settings_file = "app_settings.json"

        try:
            if os.path.exists(settings_file):
                with open(settings_file, "r") as file:
                    settings = json.load(file)
                call_reports = settings.get("native_reports", {}).get("call_reports", 0)
                sms_reports = settings.get("native_reports", {}).get("sms_reports", 0)
            else:
                call_reports = 0
                sms_reports = 0

        except Exception as e:
            kivy.logger.Logger.info(f"[ERROR] Failed to load report counts: {e}")
            call_reports = sms_reports = 0

        self.ids.user_call_reports = str(call_reports)
        self.ids.user_sms_reports = str(sms_reports)

    def export_report_files(self, selection):
        if not selection:
            MDSnackbar(
                MDLabel(
                    text="Please Select Location To Save Files",
                    text_color="brown",
                    font_size="12sp",
                    theme_text_color="Custom"
                )
            ).open()
            return

        file_path = selection[0]

        try:
            if self.report_file == "All-Crime-Reports.xlsx":
                all_reports = self.app.fireb.get_all_reports()

                if not all_reports:
                    MDSnackbar(
                        MDLabel(
                            text="No reports available to export",
                            text_color="brown",
                            font_size="12sp",
                            theme_text_color="Custom"
                        )
                    ).open()
                    return

                repos = list(all_reports.values())
                all_repos = collections.OrderedDict()
                all_repos['Reports'] = repos

                all_reports_df = pandas.DataFrame(repos)
                all_reports_path = os.path.join(file_path, "All-Crime-Reports.xlsx")
                all_reports_df.to_excel(all_reports_path, index=False)
                return MDSnackbar(
                    MDLabel(
                        text=f"{self.report_file} Exported Successfully",
                        text_color="green",
                        font_size="12sp",
                        theme_text_color="Custom"
                    )
                ).open()


            elif self.report_file == "User-Crime-Reports.xlsx":
                user_reports = self.app.fireb.get_user_reports(self.app.active_user['user'])

                if not user_reports:
                    MDSnackbar(
                        MDLabel(
                            text="No user reports available to export",
                            text_color="brown",
                            font_size="12sp",
                            theme_text_color="Custom"
                        )
                    ).open()
                    return

                user_reports_df = pandas.DataFrame(user_reports)
                user_reports_path = os.path.join(file_path, "User-Crime-Reports.xlsx")
                user_reports_df.to_excel(user_reports_path, index=False)
                return MDSnackbar(
                    MDLabel(
                        text=f"{self.report_file} Exported Successfully",
                        text_color="green",
                        font_size="12sp",
                        theme_text_color="Custom"
                    )
                ).open()


        except Exception as e:
            MDSnackbar(
                MDLabel(
                    text=f"Error: {str(e)}",
                    text_color="red",
                    font_size="12sp",
                    theme_text_color="Custom"
                )
            ).open()

        finally:
            if self.info_dialog:
                self.info_dialog.dismiss()

    def get_filechooser_dir(self, report_file):
        self.report_file = report_file
        filechooser.choose_dir(on_selection=self.export_report_files)

    def on_leave(self, *args):
        if self.selected or self.chip_data :
            self.selected = self.chip_data = None

        elif self.ids.premise_id.text or self.ids.location_id.text or self.ids.offence_id.text or self.ids.county_id.text or self.ids.time_button.text or self.ids.meta_data.text:
            self.ids.premise_id.text = self.ids.location_id.text = self.ids.offence_id.text =self.ids.county_id.text = self.ids.time_button.text = self.ids.meta_data.text = ""
        else:
            return
