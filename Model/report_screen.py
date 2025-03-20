from kivy.properties import StringProperty
from Model.database import FirebaseConnection
from Model.base_model import BaseScreenModel
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar
from libs.device import MobileFeatures


class ReportScreenModel(BaseScreenModel):
    toll_free_hotline = StringProperty("0800 722 203")
    user_crime_report = {"Category": "",
                         "Premise": "",
                         "Location": "",
                         "Offence": "",
                         "County": "",
                         "TimeOccurred": "",
                         "MetaData": ""
                 }
    crime_categories = {
        "Violent Crimes": [
            "Homicide (Murder, Manslaughter)",
            "Robbery with Violence",
            "Assault and Battery",
            "Kidnapping and Abduction",
            "Sexual and Gender-Based Violence (Rape, Defilement, Domestic Violence)"
        ],
        "Property Crimes": [
            "Burglary/Housebreaking",
            "Theft and Stealing (Pickpocketing, Carjacking)",
            "Theft by Servant",
            "Theft of Stock",
            "Arson (Setting property on fire)",
            "Vandalism and Criminal Damage"
        ],
        "Economic and Financial Crimes": [
            "Fraud and Forgery",
            "Corruption and Bribery",
            "Cybercrime (Hacking, Online Fraud, Identity Theft)",
            "Money Laundering"
        ],
        "Drug and Substance-Related Crimes": [
            "Drug Possession and Trafficking",
            "Illegal Alcohol Brewing (Chang’aa, Busaa)"
        ],
        "Public Order Offenses": [
            "Unlawful Protests and Riots",
            "Trespassing",
            "Illegal Possession of Firearms"
        ],
        "Traffic-Related Crimes": [
            "Hit and Run Accidents",
            "Drunk Driving",
            "Reckless Driving and Speeding",
            "Driving Without a License"
        ],
        "Environmental and Wildlife Crimes": [
            "Poaching",
            "Illegal Logging",
            "Pollution Violations"
        ],
        "Terrorism and National Security Crimes": [
            "Terrorist Activities",
            "Possession of Explosives",
            "Radicalization and Recruitment"
        ]
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.active_user = self.app.active_user

    def add_new_report(self, chip_data, premise, location ,offence ,county, time_occurred, meta_data):
        self.user_crime_report["Category"] =  chip_data 
        self.user_crime_report["Premise"] = premise
        self.user_crime_report["Location"] =location
        self.user_crime_report["Offence"] = offence
        self.user_crime_report["County"] = county
        self.user_crime_report["TimeOccurred"] = time_occurred
        self.user_crime_report["MetaData"] = meta_data

        rc, status = self.app.fireb.save_user_report(user_crime_report=self.user_crime_report, username=self.active_user['user'])
        if rc == 1:
            self.app.user_reported_cases = len(status.keys())

            MobileFeatures().SendUserNotification(title=self.user_crime_report['Category'],
                                                  message=self.user_crime_report['Offence'])
            # self.ids.submit_btn.disabled = False
            return MDSnackbar(MDLabel(text="Report Submitted Successfully",
                           text_color='teal',
                           theme_text_color='Custom')
                   ).open()

        else:
            # self.ids.submit_btn.disabled = False
            return MDSnackbar(MDLabel(
                text=status,
                text_color='red',
                theme_text_color='Custom')
            ).open()

