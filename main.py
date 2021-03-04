import discord
import os
import requests
import json
import random

client = discord.Client()

def getRandomName():
  # Generates a random NPC name for my dnd-ing needs using the http://names.drycodes.com/ API (for now)
  response = requests.get("http://names.drycodes.com/10?nameOptions=boy_names")

  json_data = json.loads(response.text)
  
  quote = json_data[0]
  
  return(quote.replace('_',' '))

def rollDie(number,size):
  # Rolls a NUMBER of SIZE-sided dice
  list_dice = []
  result = ''
  sum = 0
  for i in range(number):
    list_dice.append(random.randint(1,size))
  
  for i in range(number-1):
    result += str(list_dice[i])+'+'
    sum += list_dice[i]

  result += str(list_dice[number-1])
  print(result)
  sum += list_dice[number-1]

  end_string = "`"+result+"` or **"+str(sum)+"**"

  return(end_string)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  
# the commands

@client.event
async def on_message(message):
  # Command goodness
  if message.author == client.user:
    return

  if message.content.startswith('-'):
    print(message.content)

    # random name command
    if message.content == '-name':
      name = getRandomName()
      await message.channel.send(name)

    # dice rolling command
    if message.content.startswith('-r'):
      if message.content.startswith('-rd'):
        
        command = message.content + 'x'
        number = 1
        size = int(command[command.find('d')+1:-1])

      else:
        command = message.content + 'x'
        number = int(command[2:command.find('d')])
        size = int(command[command.find('d')+1:-1])
      
    await message.channel.send(rollDie(number,size))
    

client.run(os.getenv('TOKEN'))
