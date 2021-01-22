import discord
from discord import Webhook, RequestsWebhookAdapter
import os
import requests
import json
import pytz
import pymysql
from datetime import datetime, timezone
from replit import db
from keep_alive import keep_alive
from discord_webhook import DiscordWebhook, DiscordEmbed
import re


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
  res+="Ultimos 10 envíos de ***"+json_data['name']+"***\n----------------\n"
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
    await message.channel.send('>>> Hola!! Soy el bot Discord del Sistema Artemis')

  if message.content.startswith('$uvaid'):
    rawid=message.content[7:]
    print(rawid)
    id=get_uvaid(rawid)
    await message.channel.send(id)
  
  if message.content.startswith('$uvalastsubs'):
    rawid=message.content[13:]
    res=get_lastsubsbyid(rawid)
    print(res)
    await message.channel.send(">>> "+res)

  if message.content.startswith('$fecha'):
    COL = pytz.timezone('America/Bogota')
    today = datetime.now(tz=COL)
    res=today.strftime("%d/%m/%Y %H:%M:%S")
    await message.channel.send(">>> La fecha y hora actual es: "+str(res))

  if message.content.startswith('$test'):
    #https://discord.com/api/webhooks/802272889143033956/OOUuN1wyWa-c82Ez50rxqf7HRMz_IWt-_6xIW0i6vVf8xy-UhprL_oe0_v9ReFx3X--o
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/802272889143033956/OOUuN1wyWa-c82Ez50rxqf7HRMz_IWt-_6xIW0i6vVf8xy-UhprL_oe0_v9ReFx3X--o')

    # create embed object for webhook
    embed = DiscordEmbed(title='Your Title', description='Lorem ipsum dolor sit', color=242424)

    # set author
    embed.set_author(name='Guia del programador competitivo', icon_url='https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg')

    # set image
    embed.set_image(url='https://image.freepik.com/vector-gratis/libro-blanco-sobre-fondo-blanco_1308-23052.jpg')

    # set thumbnail
    embed.set_thumbnail(url='https://res.cloudinary.com/dw0butj4g/image/upload/v1611348303/gpc_nhaobw.jpg')

    # set footer
    embed.set_footer(text='Diego Rodriguez')

    # set timestamp (default is now)
    embed.set_timestamp()

    # add fields to embed
    ##embed.add_embed_field(name='Field 1', value='Lorem ipsum')
    ##embed.add_embed_field(name='Field 2', value='dolor sit')

    # add embed object to webhook
    webhook.add_embed(embed)

    response = webhook.execute()

  if message.content.startswith('$bdtest'):
    miConexion = pymysql.connect( host='freedb.tech', user= 'freedbtech_main', passwd='ecciccpl2015', db='freedbtech_artemis' )
    cur = miConexion.cursor()
    cur.execute( "SELECT tema,texto FROM temario where tema='Binary Search' ")
    for i in cur.fetchall() :
          lista=list(i)
          
          notag = re.sub("<.*?>", " ", lista[1])
          #https://discord.com/api/webhooks/802272889143033956/OOUuN1wyWa-c82Ez50rxqf7HRMz_IWt-_6xIW0i6vVf8xy-UhprL_oe0_v9ReFx3X--o
          webhook = DiscordWebhook(url='https://discord.com/api/webhooks/802272889143033956/OOUuN1wyWa-c82Ez50rxqf7HRMz_IWt-_6xIW0i6vVf8xy-UhprL_oe0_v9ReFx3X--o')

          # create embed object for webhook
          embed = DiscordEmbed(title=lista[0], description=notag, color=242424)
          lista[0]=lista[0].replace(' ','%20')
          # set author
          embed.set_author(name='Guia del programador competitivo', icon_url='https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg')

          url2='https://res.cloudinary.com/dw0butj4g/image/upload/v1611352499/'+str(lista[0])+'.png'
          
          print(url2)
          # set image
          embed.set_image(url=url2)

          # set thumbnail
          embed.set_thumbnail(url='https://res.cloudinary.com/dw0butj4g/image/upload/v1611348303/gpc_nhaobw.jpg')

          # set footer
          embed.set_footer(text='Diego Rodriguez')

          # set timestamp (default is now)
          embed.set_timestamp()

          # add fields to embed
          ##embed.add_embed_field(name='Field 1', value='Lorem ipsum')
          ##embed.add_embed_field(name='Field 2', value='dolor sit')

          # add embed object to webhook
          webhook.add_embed(embed)

          response = webhook.execute()
    miConexion.close()


keep_alive()
client.run(os.getenv('TOKEN'))

