#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

import sys
import logging

from sheep import Shepherd

from vitrine import __version__


class VitrineWorker(Shepherd):

    def initialize(self):
        self.hello_message = 'Hello, World! We are Globo.com!'

    def get_description(self):
        return 'Vitrine worker {}'.format(__version__)

    def do_work(self):
        logging.debug('Started doing work...')
        logging.info(self.hello_message)
        logging.debug('Work done!')


def main():
    worker = VitrineWorker(sys.argv[1:])
    worker.run()

if __name__ == '__main__':
    main()
