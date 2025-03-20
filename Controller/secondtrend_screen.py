import importlib
import View.SecondTrendScreen.secondtrend_screen
from Model.secondtrend_screen import SecondTrendScreenModel

# importlib.reload(View.TrendsScreen.trends_screen)


class SecondTrendScreenController:
    def __init__(self, model):
        self.model = SecondTrendScreenModel()
        self.view = View.SecondTrendScreen.secondtrend_screen.SecondTrendScreenView(controller=self, model=self.model)

    def get_view(self) -> View.SecondTrendScreen.secondtrend_screen:
        return self.view