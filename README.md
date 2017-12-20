# Rally Slackbot
_A slackbot for executing common tasks on the CA Agile Central ("Rally") platform so you never have bother with it again_

## Set-up
_coming soon_


#### todo:
- wholesale replace of 'regex' module w/ 'fuzzywuzzy'
- add set-up instructions
- expand "list all stories" for specific states
- expand "list all stories" to add defects
- dynamically obtain the current iteration
- add support for returning story-related details:
    * ~~state~~
    * status (i.e., 'Ready', 'Blocked', 'BlockedReason')
    * descriptions
    * ~~estimate~~
    * iteration
    * name 
    * ~~owner~~
    * parent (id, name, url)
    * last update
- add support for updating story-related details:
    * state
    * status (i.e., 'Ready', 'Blocked', 'BlockedReason')
    * descriptions
    * estimate
    * iteration
    * owner