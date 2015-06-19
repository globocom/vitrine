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
from vitrine.worker import GROUP_IDS

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
        user = gl.User(member.id)
        user.avatar_url = user.avatar_url.replace('s=40', 's=120')
        users.append(user)

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
    groups = []
    for id in GROUP_IDS:
        groups.append(get_group(id))
    return render_template('index.html', dt=datetime.now().strftime("%d %M %Y - %H %m %s"), groups=groups)


EXTENSION_MAP = {
    'py': ('Python', '#3581ba'),
    'pl': ('Perl', '#0298c3'),
    'groovy': ('Groovy', '#e69f56'),
    'java': ('Java', '#b07219'),
    'css': ('CSS', '#563d7c'),
    'html': ('HTML', '#e44b23'),
    'js': ('Javascript', '#f1e05a'),
    'go': ('Go', '#82937f'),
    'sh': ('Shell', '#89e051'),
    'bash': ('Bash', '#89e051'),
    'rb': ('Ruby', '#701516'),
    'c': ('C', '#555'),
    'h': ('C', '#555'),
    'cpp': ('C++', '#f34b7d'),
    'cc': ('C++', '#f34b7d'),
    'cs': ('C#', '#178600'),
    'scala': ('Scala', '#7dd3b0'),
    'erl': ('Erlang', '#0faf8d'),
    'hs': ('Haskell', '#29b544'),
    'coffee': ('Coffee', '#244776'),
    'scss': ('Scss', '#563d7c'),
    'sass': ('Sass', '#563d7c'),
    'less': ('Less', '#563d7c'),
    'sql': ('SQL', '#3F3F3F'),
    'haml': ('Haml', '#0e60e3'),
    'php': ('PHP', '#4F5D95'),
    'jsp': ('JavaServer Pages', '#b07219'),
}


def get_languages(id):
    team = Team.objects(team_id=id).first()
    if team:
        total = sum(v for (k, v) in team.languages.items() if k in EXTENSION_MAP)
        languages = []
        other = 0
        for i, (ext, count) in enumerate(sorted(team.languages.items(), key=lambda x: x[1], reverse=True)):
            if i < 4:
                if ext in EXTENSION_MAP:
                    languages.append((EXTENSION_MAP[ext], float(count) / total))
            elif ext in EXTENSION_MAP:
                other += float(count)
        if other:
            languages.append((('Outras', '#888'), other / total))
        return languages
    else:
        return []


@mod.route("/groups/<id>")
def group(id):
    users = get_group_users(id)
    group = get_group(id)
    languages = get_languages(id)
    commits = Commit.total_by_team(owner=group.name)

    return render_template('group.html', users=users, group=group, languages=languages, commits=commits)
