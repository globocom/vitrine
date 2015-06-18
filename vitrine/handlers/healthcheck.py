#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

from flask import Blueprint

from vitrine.db import do_mongoengine_healthcheck


mod = Blueprint('healthcheck', __name__)


@mod.route("/healthcheck/")
def healthcheck():
    if not do_mongoengine_healthcheck():
        return 'MONGODB is DOWN'

    return 'WORKING'
