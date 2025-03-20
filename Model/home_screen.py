from Model.base_model import BaseScreenModel
import requests
from bs4 import BeautifulSoup

class HomeScreenModel(BaseScreenModel):
    user_crime_report = {"Category": "",
                         "Premise": "",
                         "Location": "",
                         "Offence": "",
                         "County": "",
                         "Time": "",
                         "Metadata": ""
                         }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)




