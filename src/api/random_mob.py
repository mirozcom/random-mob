import logging
import os
import traceback
import pickle
from flask import Blueprint, abort, make_response, jsonify, request
from mob_group import MobGroup

storage_dir = os.environ.get('HOME_SITE', '.') + "/App_Data/mob_data"
storage_file = "saved_state.pkl"
storage_path = f"{storage_dir}/{storage_file}"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
groups: dict[str, MobGroup] = dict()

app = Blueprint('mob', __name__)


@app.route('/mob/<group>')
def group_details(group):
    if group not in groups:
        abort(make_response(jsonify("Group doesn't exist"), 404))
    mob = groups[group]
    return jsonify({
        'group': group,
        'members': mob.members,
        'roles': mob.roles
    })


@app.route('/mob/<group>/next')
def group_next(group):
    if group not in groups:
        abort(make_response(jsonify("Group doesn't exist"), 404))
    mob = groups[group]
    roles_members = mob.get_next()
    ret = {role: member for role, member in roles_members}
    save()
    return jsonify(ret)


@app.route('/mob/<group>', methods=['POST'])
def post_data(group):
    try:
        if group not in groups:
            groups[group] = MobGroup()
        mob = groups[group]
        data = request.get_json()
        mob.set_roles_members(data.get('roles', []), data.get('members', []))
        save()
        return jsonify({'members': mob.members, 'roles': mob.roles})
    except Exception as ex:
        return jsonify({'error': str(ex), 'trace': traceback.format_exception(ex)})


def save():
    with open(storage_path, 'wb') as file:
        pickle.dump(groups, file)


def load():
    global groups
    log.info(f"Loading started - groups: {';'.join(groups.keys())}")
    if not os.path.isdir(storage_dir):
        log.info(f"Creating {storage_dir}")
        os.makedirs(storage_dir)
    else:
        log.info(f"{storage_dir} exist")
    if os.path.isfile(storage_path):
        log.info(f"{storage_path} exist")
        with open(storage_path, 'rb') as file:
            groups = pickle.load(file)
    else:
        log.info(f"{storage_path} doesn't exist")
    log.info(f"Loading complete - groups: {';'.join(groups.keys())}")




