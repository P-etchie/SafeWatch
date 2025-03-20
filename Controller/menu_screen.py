import importlib
from Model.menu_screen import MenuScreenModel
import View.MenuScreen.menu_screen

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
# importlib.reload(View.MenuScreen.menu_screen)




class MenuScreenController:
    """
    The `MenuScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = MenuScreenModel()  # Model.menu_screen.MenuScreenModel
        self.view = View.MenuScreen.menu_screen.MenuScreenView(controller=self, model=self.model)

    def get_view(self) -> View.MenuScreen.menu_screen:
        return self.view
