from abc import ABCMeta, abstractmethod


class User(ABCMeta):
    @abstractmethod
    def create_user(self, name, mobile_number):
        pass

    @abstractmethod
    def show_balance(self):
        pass
