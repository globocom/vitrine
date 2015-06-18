#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

import sys
import logging
import mongoengine

from sheep import Shepherd
from gitlab import Gitlab
from dateutil import parser

from vitrine import __version__
from vitrine.models.commit import Commit
from vitrine.models.user import User


class VitrineWorker(Shepherd):

    def initialize(self):
        self.hello_message = 'Hello, World! We are Globo.com!'

    def get_description(self):
        return 'Vitrine worker {}'.format(__version__)

    def do_work(self):
        logging.debug('Started doing work...')
        logging.info(self.hello_message)
        logging.debug('Work done!')


class LangStatsWorker(Shepherd):

    def initialize(self):
        self.hello_message = 'Hello, World! I am langstats!'

    def get_description(self):
        return 'LangStats worker {}'.format(__version__)

    def do_work(self):
        logging.debug('Started doing work...')
        logging.info(self.hello_message)
        logging.debug('Work done!')


class CommitWorker(Shepherd):

    def initialize(self):
        mongoengine.connect(
            self.config.MONGODB_DB, host=self.config.MONGODB_HOST)

    def get_description(self):
        return 'Commit worker {}'.format(__version__)

    def do_work(self):

        logging.debug('Started doing work...')
        gitlab = Gitlab(self.config.GITLAB_URL, self.config.GITLAB_TOKEN)
        gitlab.auth()

        logging.info('Loading projects from gitlab...')

        for project in gitlab.Project():
            for cmt in project.Commit():

                try:
                    commit = Commit.objects.get(commit_id=cmt.id)

                    # Commit already exists.
                except:
                    commit = Commit()
                    commit.commit_id = cmt.id
                    commit.short_id = cmt.short_id
                    commit.title = cmt.title
                    commit.author_name = cmt.author_name
                    commit.author_email = cmt.author_email
                    commit.created_at = parser.parse(cmt.created_at)
                    commit.team_name = "team"
                    commit.project_id = cmt.project_id
                    commit.project_name = project.name
                    commit.save()


def main():
    worker = VitrineWorker(sys.argv[1:])
    worker.run()


def commit():
    worker = CommitWorker(sys.argv[1:])
    worker.run()

def langstats():
    worker = LangStatsWorker(sys.argv[1:])
    worker.run()

requests.packages.urllib3.disable_warnings()
