#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

from datetime import datetime

from flask import Blueprint, render_template, current_app

from vitrine.models.user import User

import gitlab


mod = Blueprint('index', __name__)

def auth():
    gl = gitlab.Gitlab(current_app.config.get('GITLAB_BASE_URL'), current_app.config.get('APP_SECRET_KEY'))
    gl.auth()
    return gl


def get_group_users(group_id):
    gl = auth()

    members = gl.Group(group_id).Member()
    users = []

    for member in members:
        users.append(gl.User(member.id))

    return users


def get_group(group_id):
    gl = auth()
    return gl.Group(group_id)


def get_all_groups():
    gl = auth()
    groups = []

    page = 0
    while True:
        g = gl.Group(page=page)
        if g:
            groups += g
        else:
            break
        page += 1

    return groups


@mod.route("/")
def index():
    groups = get_all_groups()
    return render_template('index.html', dt=datetime.now().strftime("%d %M %Y - %H %m %s"), groups=groups)


@mod.route("/groups/<id>")
def group(id):
    users = get_group_users(id);
    group = get_group(id);

    return render_template('group.html', users=users, group=group)
