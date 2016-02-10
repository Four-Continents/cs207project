# cs207project

## Branch Instructions
- Please do not make any changes on the master branch
- Please make any individual changes to files in this repo on a separate branch
- Any changes made to master will only be done with a quorum of team members
 
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
4. To merge master into your current branch type ```git merge master``` (NOTE BE CAREFUL about this. If there are any of the same files that were changed concurrently changed on your branch and master, there will be a merge conflict). 


## Collaboration Docs
1. [Trello](https://trello.com/b/WRhE0pgH/four-continents)
2. Slack Channel
