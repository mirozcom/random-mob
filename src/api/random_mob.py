import os
from flask import Flask, jsonify, request, make_response, abort
import pickle
from mob_group import MobGroup

storage_dir = "App_Data/mob_data"
storage_file = "saved_state.pkl"
storage_path = f"{storage_dir}/{storage_file}"

app = Flask(__name__)
groups: dict[str, MobGroup] = dict()


@app.route('/<group>')
def group_details(group):
    if group not in groups:
        abort(make_response(jsonify("Group doesn't exist"), 404))
    mob = groups[group]
    return jsonify({
        'group': group,
        'members': mob.members,
        'roles': mob.roles
    })


@app.route('/<group>/next')
def group_next(group):
    if group not in groups:
        abort(make_response(jsonify("Group doesn't exist"), 404))
    mob = groups[group]
    roles_members = mob.get_next()
    ret = {role: member for role, member in roles_members}
    save()
    return jsonify(ret)


@app.route('/<group>', methods=['POST'])
def post_data(group):
    if group not in groups:
        groups[group] = MobGroup()
    mob = groups[group]
    data = request.get_json()
    mob.set_roles_members(data.get('roles', []), data.get('members', []))
    save()
    return jsonify({'members': mob.members, 'roles': mob.roles})


def save():
    with open(storage_path, 'wb') as file:
        pickle.dump(groups, file)


def load():
    global groups
    if not os.path.isdir(storage_dir):
        os.makedirs(storage_dir)
    if os.path.isfile(storage_path):
        with open(storage_path, 'rb') as file:
            groups = pickle.load(file)


if __name__ == '__main__':
    load()
    app.debug = True
    app.run()
