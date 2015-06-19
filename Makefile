# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

# install all dependencies (do not forget to create a virtualenv first and activate rvm or another ruby manager)
setup: setup-ruby setup-python setup-node setup-bower

setup-python:
	@pip install -U -e .\[tests\]

setup-ruby:
	@rvm install --autolibs=3 ruby-$(shell cat .ruby-version)
	@bundle

setup-node:
	@npm install .

setup-bower:
	@cd vitrine && bower prune && bower install
	@cd vitrine && node bower_list.js

# test your application (tests in the tests/ directory)
test: mongo_test redis_test unit

unit:
	@coverage run --branch `which nosetests` -vv --with-yanc -s tests/
	@coverage report -m --fail-under=80

# show coverage in html format
coverage-html: unit
	@coverage html

# get a redis instance up (localhost:4444)
redis: kill_redis
	redis-server ./redis.conf; sleep 1
	redis-cli -p 4444 info > /dev/null

# kill this redis instance (localhost:4444)
kill_redis:
	-redis-cli -p 4444 shutdown

# get a redis instance up for your unit tests (localhost:4448)
redis_test: kill_redis_test
	@redis-server ./redis.tests.conf; sleep 1
	@redis-cli -p 4448 info > /dev/null

# kill the test redis instance (localhost:4448)
kill_redis_test:
	@-redis-cli -p 4448 shutdown

# get a mongodb instance up (localhost:3333)
mongo: kill_mongo
	@rm -rf /tmp/vitrine/mongolog
	@mkdir -p /tmp/vitrine/mongodata && mongod --dbpath /tmp/vitrine/mongodata --logpath /tmp/vitrine/mongolog --port 3333 --quiet &

# kill this mongodb instance (localhost:3333)
kill_mongo:
	@-ps aux | egrep -i 'mongod.+3333' | egrep -v egrep | awk '{ print $$2 }' | xargs kill -2

# clear all data in this mongodb instance (localhost: 3333)
clear_mongo:
	@rm -rf /tmp/vitrine && mkdir -p /tmp/vitrine/mongodata

# get a mongodb instance up for your unit tests (localhost:3334)
mongo_test: kill_mongo_test
	@rm -rf /tmp/vitrine/mongotestdata && mkdir -p /tmp/vitrine/mongotestdata
	@rm -rf /tmp/vitrine/mongotestlog
	@mongod --dbpath /tmp/vitrine/mongotestdata --logpath /tmp/vitrine/mongotestlog --port 3334 --quiet --fork --repair
	@echo 'waiting for mongo...'
	@until mongo --port 3334 --eval "quit()"; do sleep 0.25; done > /dev/null 2> /dev/null

# kill the test mongodb instance (localhost: 3334)
kill_mongo_test:
	@-ps aux | egrep -i 'mongod.+3334' | egrep -v egrep | awk '{ print $$2 }' | xargs kill -2

# run tests against all supported python versions
tox:
	@tox

#docs:
	#@cd vitrine/docs && make html && open _build/html/index.html

light_run:
	@vitrine -c vitrine/config/local.conf --debug

run: mongo light_run

