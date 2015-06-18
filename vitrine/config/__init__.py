#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

import os
from derpconf.config import Config, generate_config

STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

Config.define('APP_SECRET_KEY', None, 'SECRET KEY TO CONFIGURE vitrine', 'Security')

Config.define('WEBASSETS_DIRECTORY', STATIC_PATH, 'Folder to be root directory for webassets', 'Web')
Config.define('WEBASSETS_AUTO_BUILD', True, 'Auto build static files', 'Web')
Config.define('WEBASSETS_CACHE_PATH', '/tmp/vitrine/.webassets_cache', 'WebAssets cache path', 'Web')


Config.define('MONGODB_HOST', 'localhost', 'Host for the MongoDB database', 'MongoDB')
Config.define('MONGODB_DB', 'vitrine', 'Database name for the MongoDB database', 'MongoDB')
Config.define('MONGODB_PORT', 3333, 'Port for the MongoDB database', 'MongoDB')
Config.define('MONGODB_USERNAME', None, 'Username for the MongoDB database', 'MongoDB')
Config.define('MONGODB_PASSWORD', None, 'Password for the MongoDB database', 'MongoDB')


def init_app(app, path=None):
    conf = Config.load(path)
    for conf_option, _ in conf.items.items():
        app.config[conf_option] = conf[conf_option]

    app.secret_key = app.config['APP_SECRET_KEY']

if __name__ == '__main__':
    generate_config()
