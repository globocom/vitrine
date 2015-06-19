#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

from datetime import datetime

from flask import Blueprint, render_template, current_app

from vitrine.models.team import Team
from vitrine.models.commit import Commit

import gitlab


mod = Blueprint('index', __name__)


def auth():
    gl = gitlab.Gitlab(current_app.config.get('GITLAB_BASE_URL'), current_app.config.get('GITLAB_TOKEN'))
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

    page = 1
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


EXTENSION_MAP = {
    'py': 'Python',
    'pl': 'Perl',
    'groovy': 'Groovy',
    'java': 'Java',
    'css': 'CSS',
    'html': 'HTML',
    'js': 'Javascript',
    'go': 'Go',
    'sh': 'Shell',
    'bash': 'Bash',
    'rb': 'Ruby',
    'c': 'C',
    'h': 'C',
    'cpp': 'C++',
    'cc': 'C++',
    'cs': 'C#',
    'scala': 'Scala',
    'erl': 'Erlang',
    'hs': 'Haskell',
    'coffee': 'Coffee',
    'scss': 'Scss',
    'sass': 'Sass',
    'less': 'Less',
    'sql': 'SQL',
    'haml': 'Haml',
    'php': 'PHP',
    'jsp': 'JavaServer Pages',
}


def get_languages(id):
    team = Team.objects(team_id=id).first()
    if team:
        total = sum(team.languages.values())
        languages = []
        for ext, count in sorted(team.languages.items(), key=lambda x: x[1]):
            if ext in EXTENSION_MAP:
                languages.append((EXTENSION_MAP[ext], float(count) / total))
        return languages
    else:
        return []


@mod.route("/groups/<id>")
def group(id):
    users = get_group_users(id);
    group = get_group(id);
    languages = get_languages(id)
    commits = Commit.total_by_team(owner=group.name)

    return render_template('group.html', users=users, group=group, languages=languages, commits=commits)
