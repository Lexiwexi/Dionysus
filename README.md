# Dionysus v.0.0
Dionysus is a discord bot written in python using the discord API for python and Flask for the temporary webserver. Command Documentation will follow soon.

# Required:
- Python 3.x
- discordpy (https://discordpy.readthedocs.io/)
- Flask (https://flask.palletsprojects.com/en/1.1.x/)


# TO MAKE THIS CODE WORK...
You will need to edit the following script to contain your bot Token
- .env

Dionysus also needs to be run from a server to work, preferably repl.it as it has been developed there. The code will set up it's own webpage to keep alive for a while but will eventually shut down. This is a work in progress.

# Known Bugs:
- None so far but I am not really bugtesting yet

# Commands:

| command name       | function        |
| ------------- |-------------|
|-name | gets a random name from http://names.drycodes.com |
|-r[number]d[sides] | rolls a NUMBER of dice with SIDES-sides |
|-face| creates a face from https://campaignwiki.org/face/gallery/alex/random |
|-wipe| wipes the last 300 messages if their age does not exceed 14 days |
|-spam| spams a bunch (100) of messages |
|-coinflip [question]?[argument1]\|[argument2] | flips a coin and answers your question |
|-note [text] | saves text to the note document |
|-note| opens the note document for the user |
|-note del| wipes the note document for the user |
