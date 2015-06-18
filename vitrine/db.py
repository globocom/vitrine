#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

import logging
import sys

from flask.ext.mongoengine import MongoEngine
# from flask.ext.mongoengine import MongoEngineSessionInterface
from pymongo.errors import AutoReconnect


mongo = MongoEngine()


def do_mongoengine_healthcheck():
    conn = mongo.connection.connection
    try:
        return conn.command('ping').get('ok', 0) == 1.0
    except AutoReconnect:
        logging.exception(sys.exc_info()[1])
        return False


def init_app(app):
    logging.info('initializing db')

    app.config['MONGODB_HOST'] = app.config.get('DBAAS_MONGODB_ENDPOINT')
    mongo.init_app(app)

    if app.debug:
        app.config['DEBUG_TB_PANELS'].append('flask.ext.mongoengine.panels.MongoDebugPanel')

    # uncomment the following and related import to use mongo as session store:
    # app.session_interface = MongoEngineSessionInterface(mongo)
