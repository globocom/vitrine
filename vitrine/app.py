#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

import os
import os.path
import logging
import sys
import argparse

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from vitrine import config as config_module
from vitrine.static import assets
from vitrine import handlers, db

blueprints = (handlers, assets, db)


def run_bower_list():
    bower_list_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    bower_list = 'bower_list.js'
    try:
        os.system('cd %s && node %s' % (bower_list_path, bower_list))
    except Exception:
        err = sys.exc_info()[1]
        print "Could not update bower list of assets (%s). Shutting down." % err
        sys.exit(1)


def create_app(config, debug=False):
    app = Flask(__name__)
    app.debug = debug
    config_module.init_app(app, config)

    logging.basicConfig(level=logging.DEBUG)

    if app.debug:
        app.config['DEBUG_TB_PROFILER_ENABLED'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        app.config['DEBUG_TB_PANELS'] = app.config.get('DEBUG_TB_PANELS', [
            'flask_debugtoolbar.panels.versions.VersionDebugPanel',
            'flask_debugtoolbar.panels.timer.TimerDebugPanel',
            'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
            'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
            'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
            'flask_debugtoolbar.panels.template.TemplateDebugPanel',
            'flask_debugtoolbar.panels.logger.LoggingPanel',
            'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        ])
        app.toolbar = DebugToolbarExtension(app)

    for blueprint in blueprints:
        blueprint.init_app(app)

    if app.debug:
        run_bower_list()

    return app


def main():
    args = parse_arguments()
    app = create_app(args.conf, debug=args.debug)
    app.run(debug=args.debug, host=args.bind, port=args.port, threaded=True)


def parse_arguments(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default="3000", help="Port to start the server with.")
    parser.add_argument('--bind', '-b', default="0.0.0.0", help="IP to bind the server to.")
    parser.add_argument('--conf', '-c', default=None, help="Path to configuration file.")
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Indicates whether to run in debug mode.')

    options = parser.parse_args(args)
    return options
