#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

from datetime import datetime

from flask import Blueprint, render_template

from vitrine.models.user import User


mod = Blueprint('index', __name__)


@mod.route("/")
def index():
    users = User.objects.all()
    return render_template('index.html', dt=datetime.now().strftime("%d %M %Y - %H %m %s"), users=users)
