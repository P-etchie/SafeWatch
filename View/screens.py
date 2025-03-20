from Model.login_screen import LoginScreenModel
from Controller.login_screen import LoginScreenController
from Model.signup_screen import SignupScreenModel
from Controller.signup_screen import SignupScreenController
from Model.profile_screen import ProfileScreenModel
from Controller.profile_screen import ProfileScreenController
from Model.menu_screen import MenuScreenModel
from Controller.menu_screen import MenuScreenController
from Model.home_screen import HomeScreenModel
from Controller.home_screen import HomeScreenController
from Model.map_screen import MapScreenModel
from Controller.map_screen import MapScreenController
from Model.report_screen import ReportScreenModel
from Controller.report_screen import ReportScreenController
from Model.trends_screen import TrendsScreenModel
from Controller.trends_screen import TrendsScreenController
from Model.reset_screen import ResetScreenModel
from Controller.reset_screen import ResetScreenController
from Model.secondtrend_screen import SecondTrendScreenModel
from Controller.secondtrend_screen import SecondTrendScreenController


screens = {
    "login screen": {
        "model": LoginScreenModel,
        "controller": LoginScreenController,
    },
    "home screen": {
        "model": HomeScreenModel,
        "controller": HomeScreenController,
    },
    "map screen": {
        "model": MapScreenModel,
        "controller": MapScreenController,
    },
    "report screen": {
        "model": ReportScreenModel,
        "controller": ReportScreenController,
    },
    "profile screen": {
        "model": ProfileScreenModel,
        "controller": ProfileScreenController,
    },
    "menu screen": {
        "model": MenuScreenModel,
        "controller": MenuScreenController,
    },
    "signup screen": {
        "model": SignupScreenModel,
        "controller": SignupScreenController,
    },
    "trends screen": {
        "model": TrendsScreenModel,
        "controller": TrendsScreenController
    },
    "secondtrend screen": {
        "model": SecondTrendScreenModel,
        "controller": SecondTrendScreenController
    },
    "reset screen": {
        "model": ResetScreenModel,
        "controller": ResetScreenController,
    },
}