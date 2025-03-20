import importlib
import View.SignupScreen.signup_screen
from Model.signup_screen import SignupScreenModel

# importlib.reload(View.SignupScreen.signup_screen)


class SignupScreenController:
    def __init__(self, model):
        self.model = SignupScreenModel()
        self.view = View.SignupScreen.signup_screen.SignupScreenView(controller=self, model=self.model)

    def get_view(self) -> View.SignupScreen.signup_screen:
        return self.view
