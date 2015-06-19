#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

from vitrine.db import mongo


class Team(mongo.Document):
    team_id = mongo.IntField(primary_key=True)
    languages = mongo.MapField(mongo.IntField(verbose_name='line number'))
