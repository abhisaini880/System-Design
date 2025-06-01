from interfaces.userInterface import User as userInterface
from models.user import User
import utils


class UserService(userInterface):
    def create_user(self, name, mobile_number):
        self.user = User(
            id=utils.unique_id(), name=name, mobile_number=mobile_number
        )

        return self.user

    def show_balance(self):
        return self.user.get_balance()

    def update_balance(self, balance):
        self.user.set_balance(balance)
        return True
