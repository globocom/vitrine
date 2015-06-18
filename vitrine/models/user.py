#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

from vitrine.db import mongo


class User(mongo.Document):
    email = mongo.StringField(max_length=2000)
    username = mongo.StringField(max_length=255)
    name = mongo.StringField(max_length=255)
    user_id = mongo.StringField(required=True)
    provider = mongo.StringField(required=True)
