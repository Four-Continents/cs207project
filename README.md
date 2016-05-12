# cs207project

[![Build Status](https://travis-ci.org/Four-Continents/cs207project.svg?branch=master)](https://travis-ci.org/Four-Continents/cs207project)

[![Coverage Status](https://coveralls.io/repos/github/Four-Continents/cs207project/badge.svg?branch=master)](https://coveralls.io/github/Four-Continents/cs207project?branch=master)

In order to run tests locally, type command:
PYTHONPATH=. py.test --cov pype --cov-report term-missing
(otherwise pytest will only show timeseries, and not pype - likely some bug because the parent directory is the same name as the timeseries module. Note that changing the source in .coveragerc does not help)

## Branch Instructions
### How to git branch
1. First: git clone the repo
2. Make sure to do a ```git pull``` to get the latest from the master branch
3. To create a new branch copy from master: ```git checkout -b yourbranchname```
4. Once you have added and committed something, you can push up the branch with: ```git push --set-upstream origin yourbranchname```
5. To view all the available branches: ```git branch```
6. To switch back to master: ```git checkout master```. (Note: You will need to make sure any uncommitted changes are committed in your current branch before switching.)

### How to update your branch with master branch
1. First update master: ```git checkout master```
2. Pull into master ```git pull``` from master branch
3. Check back into your branch: ```git checkout yourbranchname```
4. To merge master into your current branch: ```git merge master``` (NOTE BE CAREFUL. If any of the same files were changed concurrently on your branch and master, you will need to manually resolve merge conflicts). 

## Collaboration Docs
1. [Trello](https://trello.com/b/WRhE0pgH/four-continents)