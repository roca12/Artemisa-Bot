import discord
import os
import requests
import json


client = discord.Client()

def get_uvaid(uvausername):
  response=requests.get("https://uhunt.onlinejudge.org/api/uname2uid/"+uvausername+"")
  json_data=json.loads(response.text)
  userid="El id del usuario "+uvausername+" es "+str(json_data)
  return (userid)

def get_uvaidutil(uvausername):
  response=requests.get("https://uhunt.onlinejudge.org/api/uname2uid/"+str(uvausername)+"")
  json_data=json.loads(response.text)
  userid=json_data
  return (userid)

def get_lastsubsbyid(uvaid):
  id=get_uvaidutil(uvaid);
  response=requests.get("https://uhunt.onlinejudge.org/api/subs-user-last/"+str(id)+"/10")
  print(id)
  print("https://uhunt.onlinejudge.org/api/subs-user-last/"+str(id)+"/10")
  json_data=json.loads(response.text)
  return json_data

@client.event
async def on_ready():
  print('Logueado como {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author==client.user:
    return

  if message.content.startswith('$hola'):
    await message.channel.send('Hola!! Soy el bot Discord del Sistema Artemis')

  if message.content.startswith('$uvaid'):
    rawid=message.content[7:]
    print(rawid)
    id=get_uvaid(rawid)
    await message.channel.send(id)
  
  if message.content.startswith('$uvalastsubs'):
    rawid=message.content[13:]
    res=get_lastsubsbyid(rawid)
    print(res)
    await message.channel.send(res)

client.run(os.getenv('TOKEN'))
