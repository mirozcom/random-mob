import random
from itertools import permutations


class MobGroup:
    def __init__(self):
        self.members = []
        self.roles = []
        self.set_keys = []
        self.total_roles = {}
        self.per_role = {}
        self.total_sets = {}
        self.last_member_appearance = {}
        self.last_appearance_in_role = {}
        self.last_set_appearance = {}

    def set_roles_members(self, roles, members):
        self.members = members
        self.roles = roles
        self.set_keys = [f"{p[0]}:{p[1]}" for p in permutations(members, 2)]
        self.total_roles: dict[str, int] = {m: 0 for m in members}
        self.per_role: dict[str, dict[str, int]] = {r: {m: 0 for m in members} for r in roles}
        self.total_sets: dict[str, int] = {k: 0 for k in self.set_keys}
        self.last_member_appearance: dict[str, int] = {m: 0 for m in members}
        self.last_appearance_in_role: dict[str, dict[str, int]] = {r: {m: 0 for m in members} for r in roles}
        self.last_set_appearance: dict[str, int] = {k: 0 for k in self.set_keys}

    def get_next(self):
        roles_members = get_next_pair(self.members, self.roles, self.total_roles, self.per_role, self.total_sets, self.last_member_appearance, self.last_appearance_in_role, self.last_set_appearance)
        return roles_members


def get_next_pair(members, roles, total_roles, per_role, total_sets, last_member_appearance, last_appearance_in_role,
                  last_set_appearance):
    roles_members = pick_next(members, roles, total_roles, per_role, total_sets, last_member_appearance,
                              last_appearance_in_role, last_set_appearance)
    for member in last_member_appearance:
        last_member_appearance[member] += 1
    for role in roles:
        for member in last_appearance_in_role[role]:
            last_appearance_in_role[role][member] += 1
    for key in last_set_appearance:
        last_set_appearance[key] += 1
    for role, member in roles_members:
        total_roles[member] += 1
        per_role[role][member] += 1
        last_member_appearance[member] = 0
        last_appearance_in_role[role][member] = 0
    key = ":".join(m[1] for m in roles_members)
    last_set_appearance[key] = 0
    total_sets[key] = total_sets.get(key, 0) + 1
    return roles_members


def reduct_values_dict(values: dict[str, int]):
    min_total = min(values.values()) if len(values) else 0
    return {key: value - min_total for key, value in values.items()}


def pick_next(members, roles, total_roles, per_role, total_sets, last_appearance, last_appearance_in_role, last_set_appearance):
    roles_members = []
    all_members = list(members)
    total_roles = reduct_values_dict(total_roles)
    per_role = {role: reduct_values_dict(values) for role, values in per_role.items()}
    total_sets = reduct_values_dict(total_sets)
    last_appearance = reduct_values_dict(last_appearance)
    last_appearance_in_role = {role: reduct_values_dict(values) for role, values in last_appearance_in_role.items()}
    last_set_appearance = reduct_values_dict(last_set_appearance)
    prefix_key = ""
    for role in roles:
        weights = [
            (
                    ((last_appearance[m] + 1) ** 0)  # set to 0 to ignore last appearance for now
                    * ((last_appearance_in_role[role][m] + 1) ** 0)  # set to 0 to ignore last appearance for now
                    * ((last_set_appearance.get(f"{prefix_key}:{m}", 0) + 1) ** 0)  # set to 0 to ignore last appearance for now
            )
            /
            (
                    ((total_roles[m] + 1) ** 10)
                    * ((per_role[role][m] + 1) ** 10)
                    * ((total_sets.get(f"{prefix_key}:{m}", 0) + 1) ** 10)
            )
            for m in all_members
        ]
        member = random.choices(all_members, weights, k=1)[0]
        all_members.remove(member)
        roles_members.append((role, member))
        prefix_key = ":".join(m[1] for m in roles_members)
    return roles_members
