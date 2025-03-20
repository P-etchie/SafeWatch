from Model.base_model import BaseScreenModel
from Model.database import FirebaseConnection
from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar


class SignupScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.signup_screen.SignupScreen.SignupScreenView` class.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.app = None


    # def register_new_user(self, fullnameId, usernameId, emailId, pass_field1,
    #                       pass_field2, phoneID, addressId):
    #     rCode, status = self.firebase_connection.register_new_user(fullnameId, usernameId, emailId, pass_field1,
    #                       pass_field2, phoneID, addressId)
    #     if not rCode:
    #         return



