from src.api.mob_group import MobGroup

g = MobGroup()
g.set_roles_members(["AAA", "BBB"], ["Prvi", "Drugi", "Treci", "Cetrvti"])
for i in range(100):
    values = g.get_next()
    print(values)
