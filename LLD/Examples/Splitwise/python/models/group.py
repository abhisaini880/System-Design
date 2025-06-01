""" Group Model Entity """

from enum import Enum


class GroupStatus(Enum):
    active = "ACTIVE"
    closed = "CLOSED"


class Group:
    def __init__(self, id, name):
        self._name = name
        self._id = id
        self.members = []
        self.balances = {}
        self.expenses = []
        self.status = GroupStatus.active

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    name = property(get_name, set_name)
    id = property(get_id)
