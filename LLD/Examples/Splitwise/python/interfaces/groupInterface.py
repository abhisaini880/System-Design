from abc import ABCMeta, abstractmethod


class Group(ABCMeta):
    @abstractmethod
    def create_group(self, name):
        pass

    @abstractmethod
    def add_member(self, user):
        pass

    @abstractmethod
    def show_balance(self):
        pass

    @abstractmethod
    def get_group_status(self):
        pass

    @abstractmethod
    def close_group(self):
        pass
