import importlib
from Model.report_screen import ReportScreenModel
import View.ReportScreen.report_screen

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.ReportScreen.report_screen)




class ReportScreenController:
    """
    The `ReportScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = ReportScreenModel()
        self.view = View.ReportScreen.report_screen.ReportScreenView(controller=self, model=self.model)

    def get_view(self) -> View.ReportScreen.report_screen:
        return self.view
