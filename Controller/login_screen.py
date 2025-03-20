import importlib
from Model.login_screen import LoginScreenModel
import View.LoginScreen.login_screen

# importlib.reload(View.LoginScreen.login_screen)




class LoginScreenController:
    """
    The `LoginScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = LoginScreenModel()
        self.view = View.LoginScreen.login_screen.LoginScreenView(controller=self, model=self.model)

    def get_view(self) -> View.LoginScreen.login_screen:
        return self.view
