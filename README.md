# SF-SirenBot
ServerForge's OSS SirenBot. Monitor dangerous changes in your communities and be alerted as soon as they happen.

## To Do: 
### Events
* New users added to watched roles
* Users in watched roles kicked/banned
* Users in watched roles losing any roles
* Users in watched roles' activity.
* New webhooks created
* Any bots removed (or this bot itself removed)
* Any role being given any of the following perms: `administrator`, `manage_roles`, `mention_everyone`, `manage_webhooks`, `manage_channels`, `manage_server`.
* Watch general chat to see if it gets locked. (Send messages or view channel disabled for verified role or @ everyone)
* How many people are boosting the server / if the server is about to lose a boost

### Commands
* /register modrole role:@role
* /register adminrole role:@role
* /register teamrole role:@role
* /register generalchannel channel:#general
* /register verifiedrole role:@role

### Functions
* Send a webhook to command server (hardcoded in) when the activity above happens.
* Send a webhook to command server when specific really bad activity happens.
* Send a webhook to command server every day at noon with user activity recorded. I.e. a text based graph that looks like this, with each mod having their own thread in a specific channel

> ![image](https://user-images.githubusercontent.com/57507687/217126127-9deee77d-3df3-4e3d-baef-0bff8cb2a7f5.png)

*X emoji means offline. Red square means DND mode. Green means online. Orange means idle. Purple means online (any status) any % of time but not online more than 50% of the hour.*

### Additional
* Help menu
* Fix the issue where the `help` command falls under 'No Category' in the help menu. I (Pattles) have just added a janky fix for the time being, visible in SirenBot.py

## Completed
After an item is completed from the [To Do](https://github.com/ping-Toven/SF-SirenBot/blob/main/README.md#to-do) list, *italicize* it, then add it below.
* Test item - Pattles

## Additional Information
### Permissions Required
* View Channels
* View Audit Log *(for webhook logging)*
* Read Messages
* Send Messages
* Read Message History
