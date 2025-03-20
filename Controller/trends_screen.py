import importlib
import View.TrendsScreen.trends_screen
from Model.trends_screen import TrendsScreenModel

# importlib.reload(View.TrendsScreen.trends_screen)


class TrendsScreenController:
    """
    The `SignupScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = TrendsScreenModel()
        self.view = View.TrendsScreen.trends_screen.TrendsScreenView(controller=self, model=self.model)

    def get_view(self) -> View.TrendsScreen.trends_screen:
        return self.view
