from Model.reset_screen import ResetScreenModel
from View.ResetScreen.reset_screen import ResetScreenView

class ResetScreenController:
    def __init__(self, model):
        self.model = ResetScreenModel()
        self.view = ResetScreenView(controller=self, model=self.model)

    def get_view(self):
        return self.view