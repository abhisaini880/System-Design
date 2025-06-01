from interfaces.groupInterface import Group as groupInterface
from models.group import Group, GroupStatus
import utils


class GroupService(groupInterface):
    def create_group(self, name):
        self.group = Group(name=name, id=utils.unique_id())
        return self.group

    def add_member(self, user):
        self.group.members.append(user)

    def show_balance(self):
        return self.group.balances

    def get_group_status(self):
        return self.group.status

    def close_group(self):
        if any(self.group.balances.values()):
            print("Group expenses are not settled! please settle-up first.")
            return False
        self.group.status = GroupStatus.closed
