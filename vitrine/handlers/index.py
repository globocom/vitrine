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


def get_group_users(group_id):
    gl = gitlab.Gitlab(current_app.config.get('GITLAB_BASE_URL'), current_app.config.get('APP_SECRET_KEY'))
    gl.auth()

    members = gl.Group(group_id).Member()
    users = []

    for member in members:
        users.append(gl.User(member.id))

    return users


@mod.route("/")
def index():
    users = User.objects.all()a
    return render_template('index.html', dt=datetime.now().strftime("%d %M %Y - %H %m %s"), users=users)
