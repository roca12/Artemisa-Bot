import discord
import os
import requests
import json
import pytz
from datetime import datetime, timezone
from tzlocal import get_localzone


client = discord.Client()
veredictos={"10" : "Submission error",
"15" : "Can't be judged",
"20" : "In queue",
"30" : "Compile error",
"35" : "Restricted function",
"40" : "Runtime error",
"45" : "Output limit",
"50" : "Time limit",
"60" : "Memory limit",
"70" : "Wrong answer",
"80" : "Presentation Error",
"90" : "Accepted"}

lenguajesuva={"1":"ANSI C","2":"JAVA","3":"C++","4":"PASCAL","5":"C++11"}

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
  res=""
  res+="Ultimos 10 envíos de "+json_data['name']+"\n----------------\n"
  subs=json_data['subs']
  for i in subs:
    response2=requests.get("https://uhunt.onlinejudge.org/api/p/id/"+str(i[1]))
    problem_data=json.loads(response2.text)
    res+="Id de envío: "+str(i[0])+"\n"
    res+="Id del problema: "+str(problem_data["num"])+"\n"
    res+="Nombre del problema: "+str(problem_data["title"])+"\n"
    res+="Veredicto: "+str(veredictos[str(i[2])])+"\n"
    res+="Lenguaje: "+str(lenguajesuva[str(i[5])])+"\n"
    res+="\n"
  return res

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

  if message.content.startswith('$fecha'):
    COL = pytz.timezone('America/Bogota')
    today = datetime.now(tz=COL)
    res=today.strftime("%d/%m/%Y %H:%M:%S")
    await message.channel.send("La fecha y hora actual es: "+str(res))

client.run(os.getenv('TOKEN'))
