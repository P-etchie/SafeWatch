import importlib
import View.HomeScreen.home_screen
from Model.home_screen import HomeScreenModel
# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.HomeScreen.home_screen)


class HomeScreenController:


    def __init__(self, model):
        self.model = HomeScreenModel()# Model.home_screen.HomeScreenModel
        self.view = View.HomeScreen.home_screen.HomeScreenView(controller=self, model=self.model)

    def get_view(self) -> View.HomeScreen.home_screen:
        return self.view
