class Group:
    """

    members = {
        "test1": {
            "test2": +10
            "test3": -20
        },
        "test2": {
            "test1": -10
        },
        "test3": {
            "test1": +20
        }
    }


    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.members = {}

    def add_member(self, user):
        self.members[user] = {}

    def add_expense(self, paid_by, amount: int):
        contri = amount / len(self.members)

        for member in self.members.keys():
            if member == paid_by:
                for child_member in self.members.keys():
                    if child_member == paid_by:
                        continue
                    if child_member not in self.members[paid_by]:
                        self.members[paid_by][child_member] = 0

                    self.members[paid_by][child_member] += round(contri, 2)

            else:
                self.members[member][paid_by] = (
                    round(self.members[member][paid_by] - contri, 2)
                    if self.members[member].get(paid_by)
                    else round(0 - contri, 2)
                )

    def simplify(self):
        for member, data in self.members.items():
            for child_member, bal in data.items():
                pass


class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.groups = []

    def add_to_group(self, group):
        self.groups.append(group)


# class Transaction:
#     def __init__(self) -> None:
#         self.transactios

#     def add_transaction(self, date, amount, paid_by):


class Splitwise:
    def __init__(self) -> None:
        self.groups = []
        self.users = []

    def create_group(self, group_name: str):
        group = Group(group_name)
        self.groups.append(group)
        return group

    def display_groups(self):
        for group in self.groups:
            print(group.name)
            print(f"Group Members: {len(group.members)}")
            for member, bal in group.members.items():
                for c_member, bal in bal.items():
                    if bal < 0:
                        print(
                            f"{member.name} has to pay Rs.{abs(bal)} to {c_member.name}"
                        )
                    else:
                        print(
                            f"{member.name} has to receive Rs.{abs(bal)} from {c_member.name}"
                        )
            print("")

    def create_user(self, user_name: str):
        user = User(user_name)
        self.users.append(user)
        return user

    def add_user_in_group(self, user: User, group: Group):
        user.add_to_group(group)
        group.add_member(user)

    def add_expense(self, user: User, group: Group, amount: int):
        group.add_expense(user, amount)


if __name__ == "__main__":
    s = Splitwise()

    g1 = s.create_group("test1")
    g2 = s.create_group("test2")

    u1 = s.create_user("ABHI")
    u2 = s.create_user("ABHI2")
    u3 = s.create_user("ABHI3")
    u4 = s.create_user("ABHI4")
    u5 = s.create_user("ABHI5")

    s.add_user_in_group(u1, g1)
    s.add_user_in_group(u2, g1)
    s.add_user_in_group(u3, g1)
    s.add_user_in_group(u1, g2)
    s.add_user_in_group(u4, g2)
    s.add_user_in_group(u5, g2)

    s.add_expense(u1, g1, 120)
    s.add_expense(u2, g1, 90)
    s.add_expense(u3, g1, 300)

    s.display_groups()
