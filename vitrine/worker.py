#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

import sys
import logging
import gitlab
import mongoengine
import collections

from models.team import Team
from sheep import Shepherd
from dateutil import parser

from vitrine import __version__, config
from vitrine.models.commit import Commit


IGNORE = {
    'conf',
    'config',
    'txt',
    'lock',
    'project',
    'wiki',
    'properties',
    'gems',
    'gemspec',
    'rspec',
    'patch',
    'globo',
    'ico',
    'jpeg',
    'gif',
    'jpg',
    'png',
    'hosts',
    'empty',
    'localhost',
    'loopback',
    'base',
    'apt',
    'ca',
    'unfiltered',
    'setup',
    'init',
    'class',
    'jar',
    'swf',
    'bz2',
    'zip',
    'sqlite',
    'bkp',
    'war',
    'pyc',
    'db',
    'example',
    'egg',
    'vcproj',
}

GROUP_IDS = [9, 33, 88, 15, 14, 102]


def _get_projects(gl):
    projects = []
    for group_id in GROUP_IDS:
        projects.extend(gl.Group(group_id).projects)
    return projects


class LangStatsWorker(Shepherd):

    def initialize(self):
        self.gl = gitlab.Gitlab(
            self.config.GITLAB_BASE_URL, self.config.GITLAB_TOKEN)
        mongoengine.connect(host=self.config.DBAAS_MONGODB_ENDPOINT)
        self.gl.auth()
        self.runs = 0
        self.teams_seen = set()

    def get_description(self):
        return 'LangStats worker {}'.format(__version__)

    def _get_lines(self, project, path):
        try:
            return 1  # project.blob('master', filepath=path).count('\n')
        except:
            print project.id, path
            return 1

    def _walk(self, current_node, project, extensions, path):
        for file_ in current_node:
            if path:
                new_path = '/'.join([path, file_['name']])
            else:
                new_path = file_['name']
            if file_['type'] == 'tree':
                self._walk(
                    project.tree(path=new_path, ref_name='master'), project, extensions, new_path)
            else:
                exts = file_['name'].split('.')
                if len(exts) > 1 and exts[0] and exts[-1].lower() not in IGNORE:
                    extensions[
                        exts[-1].lower()] += self._get_lines(project, new_path)

    def _lang_stats(self, project):
        extensions = collections.defaultdict(lambda: 0)
        try:
            current_node = project.tree(ref_name='master')
        except gitlab.GitlabGetError:
            return {}
        else:
            self._walk(current_node, project, extensions, '')
            return extensions

    def _process_project(self, project):
        team = Team.objects(team_id=project.namespace.id).first()
        # We reset team statistics when we first encounter it
        if project.namespace.id not in self.teams_seen:
            team.delete()
            team = None
            self.teams_seen.add(project.namespace.id)
        if not team:
            team = Team(team_id=project.namespace.id)
        for (lang, total) in self._lang_stats(project).items():
            if lang in team.languages:
                team.languages[lang] += total
            else:
                team.languages[lang] = total
        team.save()

    def do_work(self):
        logging.debug('Started doing work...')
        for project in _get_projects(self.gl):
            self._process_project(project)
        logging.debug('Work done!')
        self.teams_seen = set()


class CommitsWorker(Shepherd):

    def initialize(self):

        self.gl = gitlab.Gitlab(
            self.config.GITLAB_BASE_URL, self.config.GITLAB_TOKEN)
        mongoengine.connect(host=self.config.DBAAS_MONGODB_ENDPOINT)

    def get_description(self):
        return 'Commits worker {}'.format(__version__)

    def do_work(self):

        logging.info('Loading projects from Gitlab...')

        for project in _get_projects(self.gl):
            for page in range(1, 20):  # Missing total commits...
                for cmt in project.Commit(page=page, per_page=100):

                    try:
                        commit = Commit.objects.get(commit_id=cmt.id)

                    except:

                        # Object commit does not exists.
                        commit = Commit()
                        commit.commit_id = cmt.id
                        commit.short_id = cmt.short_id
                        commit.title = cmt.title
                        commit.author_name = cmt.author_name
                        commit.author_email = cmt.author_email
                        commit.created_at = parser.parse(cmt.created_at)
                        commit.owner = project.namespace.name
                        commit.project_id = cmt.project_id
                        commit.project_name = project.name
                        commit.save()


def commits():
    worker = CommitsWorker(sys.argv[1:])
    worker.run()


def langstats():
    worker = LangStatsWorker(sys.argv[1:])
    worker.run()
