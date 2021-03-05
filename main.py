import discord
import os
import requests
import json
import random
import shutil
from PIL import Image, ImageDraw, ImageFilter
from keep_alive import keep_alive

# https://discordpy.readthedocs.io/en/latest/api.html#discord.Message.content

client = discord.Client()

def getRandomName():
  # Generates a random NPC name for my dnd-ing needs
  x = random.randint(0,1)
  if x == 1:
    response = requests.get("http://names.drycodes.com/10?nameOptions=boy_names")
  if x == 0:
    response = requests.get("http://names.drycodes.com/10?nameOptions=girl_names")

  json_data = json.loads(response.text)
  
  quote = json_data[0]
  
  return(quote.replace('_',' '))

def rollDie(number,size):
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

def remove_transparency(im, bg_colour=(255, 255, 255)):
#  this code was (shamelessly) stolen from: https://stackoverflow.com/questions/35859140/remove-transparency-alpha-from-any-image-using-pil
    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im

def getRandomFace():
  image_url = ''
  #https://campaignwiki.org/face/render/alex/eyes_all_10.png_,mouth_all_10.png,chin_man_10.png_,ears_all_10.png_,nose_man_woman_dwarf_10.png_,hair_man_10.png

  face_parts_fe = [
    'eyes_all_',
    'mouth_all_',
    'chin_woman_',
    'ears_all_',
    'nose_man_woman_dwarf_',
  ]
  face_parts_ma = [
    'eyes_all_',
    'mouth_all_',
    'chin_man_',
    'ears_all_',
    'nose_man_woman_dwarf_',
  ]

  hair_num = random.randint(1,4)
  gen_num = random.randint(1,2)
  if gen_num == 1:
    hair = 'hair_man_'+str(hair_num*5)
    for i in range(len(face_parts_ma)):
      num = random.randint(1,5)
      print(face_parts_ma[i]+str(num))
      image_url += face_parts_ma[i]+str(num)+'.png,'
  if gen_num == 2:
    hair = 'hair_woman_'+str(hair_num*5)

    for i in range(len(face_parts_fe)):
      num = random.randint(1,5)
      print(face_parts_fe[i]+str(num))
      image_url += face_parts_fe[i]+str(num)+'.png,'

  image_url = "https://campaignwiki.org/face/render/alex/"+image_url+hair+'.png'

  
  
  filename = 'face_image.png'
  r = requests.get(image_url, stream = True)

  if r.status_code == 200:
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    r.raw.decode_content = True
    
    # Open a local file with wb ( write binary ) permission.
    with open(filename,'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    print('Image sucessfully Downloaded: ',filename)
  else:
    print('Image Couldn\'t be retreived')

  print(filename)
  image = Image.open(filename)
  image = remove_transparency(image)
  image.save(filename)
  

  return(filename)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

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
    
    if message.content == '-face':
      face = getRandomFace()

      await message.channel.send(file=discord.File(face))
keep_alive()

client.run(os.getenv('TOKEN'))
