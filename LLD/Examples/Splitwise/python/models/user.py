""" User Model Entity """


class User:
    def __init__(self, id, name, mobile_number):
        self._id = id
        self._name = name
        self._mobile_number = mobile_number
        self._balance = 0

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_mobile_number(self):
        return self._mobile_number

    def get_balance(self):
        return self._balance

    def set_balance(self, balance):
        self._balance = balance

    name = property(get_name)
    id = property(get_id)
    mobile_number = property(get_mobile_number)
