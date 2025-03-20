import importlib
from Model.profile_screen import ProfileScreenModel
import View.ProfileScreen.profile_screen

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.ProfileScreen.profile_screen)




class ProfileScreenController:
    """
    The `ProfileScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = ProfileScreenModel()  # Model.profile_screen.ProfileScreenModel
        self.view = View.ProfileScreen.profile_screen.ProfileScreenView(controller=self, model=self.model)

    def get_view(self) -> View.ProfileScreen.profile_screen:
        return self.view
