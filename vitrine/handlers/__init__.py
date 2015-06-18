#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>


from vitrine.handlers import (
    healthcheck,
    index,
    # add your own handlers here
)


def init_app(app):
    app.register_blueprint(healthcheck.mod)
    app.register_blueprint(index.mod)
