import discord
import os
import requests
import json
import pytz
import pymysql
import sqlite3
from datetime import datetime
from replit import db
from keep_alive import keep_alive
import re

client = discord.Client()
veredictos = {
    "10": "Submission error",
    "15": "```diff\n- Can't be judged\n```",
    "20": "```diff\n- In queue\n```",
    "30": "```diff\n- Compile error\n```",
    "35": "```diff\n- Restricted function\n```",
    "40": "```diff\n- Runtime error\n```",
    "45": "```diff\n- Output limit\n```",
    "50": "```diff\n- Time limit\n```",
    "60": "```diff\n- Memory limit\n```",
    "70": "```diff\n- Wrong answer\n```",
    "80": "```diff\n- Presentation Error\n```",
    "90": "```diff\n+ Accepted\n```"
}

lenguajesuva = {
    "1": "ANSI C",
    "2": "JAVA",
    "3": "C++",
    "4": "PASCAL",
    "5": "C++11"
}


    

def get_uvaid(uvausername):
    response = requests.get("https://uhunt.onlinejudge.org/api/uname2uid/" +
                            uvausername + "")
    json_data = json.loads(response.text)
    userid = "El id del usuario " + uvausername + " es " + str(json_data)
    return (userid)


def get_uvaidutil(uvausername):
    response = requests.get("https://uhunt.onlinejudge.org/api/uname2uid/" +
                            str(uvausername) + "")
    json_data = json.loads(response.text)
    userid = json_data
    return (userid)


def get_lastsubsbyid(uvaid):
    id = get_uvaidutil(uvaid)
    response = requests.get(
        "https://uhunt.onlinejudge.org/api/subs-user-last/" + str(id) + "/10")
    print(id)
    print("https://uhunt.onlinejudge.org/api/subs-user-last/" + str(id) +
          "/10")
    json_data = json.loads(response.text)
    res = ""
    res += "Ultimos 10 envíos de ***" + json_data[
        'name'] + "***\n----------------\n"
    subs = json_data['subs']
    for i in subs:
        response2 = requests.get("https://uhunt.onlinejudge.org/api/p/id/" +
                                 str(i[1]))
        problem_data = json.loads(response2.text)
        res += "Id de envío: " + str(i[0]) + "\n"
        res += "Id del problema: " + str(problem_data["num"]) + "\n"
        res += "Nombre del problema: " + str(problem_data["title"]) + "\n"
        res += "Veredicto: " + str(veredictos[str(i[2])]) + "\n"
        res += "Lenguaje: " + str(lenguajesuva[str(i[5])]) + "\n"
        res += "\n"
    return res


@client.event
async def on_ready():
    print('Logueado como {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
      return
    
      
        
    if message.content.startswith('$help') or message.content.startswith('$ayuda'):
      embed = discord.Embed(
          title="lIsta de comandos",  color=242424)

      embed.set_author(
          name='Artemis BOT',
          icon_url='https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
      )
      embed.add_field(name="$help o &ayuda", value="Muestra la lista de comandos del BOT", inline=False)
      embed.add_field(name="$uvaid [uvausername]", value="Retorna el id de la cuenta de UVa Online Judge", inline=False)
      embed.add_field(name="$uvalastsubs  [uvausername]", value="Retorna los ultimos 10 envios de la cuenta de UVa Online Judge", inline=False)
      embed.add_field(name="$fecha", value="Muestra la fecha y hora actual", inline=False)
      embed.add_field(name="$test", value="Testea la conexión a la base de datos", inline=False)
      embed.add_field(name="$listatemas [pagina]", value="Muestra la lista de temas dentro de la base de datos (Paginas desde la 1 a la 5, cualquier otro numero no es valido)", inline=False)
      embed.add_field(name="$hola", value="Registra tu entrada en la base de datos (Usalo cuando vayas a entrar a una clase)", inline=False)
      embed.add_field(name="$chao", value="Registra tu salida en la base de datos (Usalo cuando vayas a salir a una clase)", inline=False)
      embed.add_field(name="$listaestudiantesentrada", value="(Solo profesores y administrador) muestra la lista de entradas de participantes a clase", inline=False)
      embed.add_field(name="$listaestudiantessalida", value="(Solo profesores y administrador) muestra la lista de salidas de participantes a clase", inline=False)
      embed.add_field(name="$borrarlistado", value="(Solo profesores y administrador) borra las listas de entrada y salida de participantes", inline=False)

      await message.channel.send(embed=embed)

    if message.content.startswith('$hola'):
      usuario=message.author.display_name
      print(usuario)
      
      await message.channel.send(
            '>>> Hola '+usuario+'!! Soy el bot Discord del Sistema Artemis')
       
      con = sqlite3.connect('mydatabase.db')

      cursorObj = con.cursor()
      cursorObj.execute("CREATE TABLE if not exists saludos(id integer PRIMARY KEY, name text, fecha text)")
      con.commit()

      cursorObj = con.cursor()
      COL = pytz.timezone('America/Bogota')
      today = datetime.now(tz=COL)
      res = today.strftime("%d/%m/%Y %H:%M:%S")
      cursorObj.execute('SELECT COUNT(*) from saludos')
      cur_result = cursorObj.fetchone()
      rows = cur_result[0]
      print(rows)
      entities = (rows+1, usuario,str(res) )
      cursorObj.execute('INSERT INTO saludos(id, name, fecha) VALUES(?, ?, ?)', entities)
      con.commit()

      cursorObj = con.cursor()
      cursorObj.execute('SELECT * FROM saludos')
      rows = cursorObj.fetchall()
      for row in rows:
        print(row)
      await message.channel.send(
            '>>> Registrada entrada de '+usuario+'!! con fecha y hora '+str(res))

    if message.content.startswith('$chao'):
      usuario=message.author.display_name
      print(usuario)
       
      con = sqlite3.connect('mydatabase.db')

      cursorObj = con.cursor()
      cursorObj.execute("CREATE TABLE if not exists salidas(id integer PRIMARY KEY, name text, fecha text)")
      con.commit()

      cursorObj = con.cursor()
      COL = pytz.timezone('America/Bogota')
      today = datetime.now(tz=COL)
      res = today.strftime("%d/%m/%Y %H:%M:%S")
      cursorObj.execute('SELECT COUNT(*) from salidas')
      cur_result = cursorObj.fetchone()
      rows = cur_result[0]
      print(rows)
      entities = (rows+1, usuario,str(res) )
      cursorObj.execute('INSERT INTO salidas(id, name, fecha) VALUES(?, ?, ?)', entities)
      con.commit()

      cursorObj = con.cursor()
      cursorObj.execute('SELECT * FROM salidas')
      rows = cursorObj.fetchall()
      for row in rows:
        print(row)
      await message.channel.send(
            '>>> Registrada salida de '+usuario+'!! con fecha y hora '+str(res))

    if message.content.startswith('$listaestudiantesentrada'):
      roles=message.author.roles
      admin=False
      for rol in roles:
        if rol.name=='Administrador' or rol.name=='Profesor':
            admin=True
            break;
      if admin:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM saludos')
        rows = cursorObj.fetchall()
        await message.channel.send(
                  '>>> Listando hora entrada de participantes\n')
        if len(rows)==0:
          await message.channel.send(
                  '>>> --- No hay datos :3 ---\n')
        for row in rows:
          await message.channel.send(
                  '>>> '+row[1]+' -> '+row[2]+'')  
      else:
        await message.channel.send(">>> No tienes permisos para ejecutar este comando")

    if message.content.startswith('$listaestudiantessalida'):
      roles=message.author.roles
      admin=False
      for rol in roles:
        if rol.name=='Administrador' or rol.name=='Profesor':
            admin=True
            break;
      if admin:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM salidas')
        rows = cursorObj.fetchall()
        await message.channel.send(
                  '>>> Listando hora salida de participantes\n')
        if len(rows)==0:
          await message.channel.send(
                  '>>> --- No hay datos :3 ---\n')
        for row in rows:
          await message.channel.send(
                  '>>> '+row[1]+' -> '+row[2]+'')  
      else:
        await message.channel.send(">>> No tienes permisos para ejecutar este comando")

    if message.content.startswith('$borrarlistado'):
      roles=message.author.roles
      admin=False
      for rol in roles:
        if rol.name=='Administrador' or rol.name=='Profesor':
            admin=True
            break;
      if admin:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()

        try:
          cursorObj.execute('DELETE FROM saludos')
          cursorObj.execute('DELETE FROM salidas')
          con.commit()
          await message.channel.send(
                  '>>> Listados borrados correctamente, listos para la siguiente clase\n')
        except sqlite3.Error:
          print(sqlite3.Error)
          await message.channel.send(
                  '>>> Error al borrar las listas, puede que ya hayan sido borradas\n')
      else:
        await message.channel.send(">>> No tienes permisos para ejecutar este comando")
            
    if message.content.startswith('$uvaid'):
        rawid = message.content[7:]
        print(rawid)
        id = get_uvaid(rawid)
        await message.channel.send(id)

    if message.content.startswith('$uvalastsubs'):
        rawid = message.content[13:]
        res = get_lastsubsbyid(rawid)
        print(res)
        embed = discord.Embed(title=rawid, description=res, color=242424)

        embed.set_author(name='Online Judge')

        embed.set_thumbnail(
            url=
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJgISMZhBm1WWetW5JWIgcGGhTv6y5O8JBKQ&usqp=CAUhttps://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJgISMZhBm1WWetW5JWIgcGGhTv6y5O8JBKQ&usqp=CAU'
        )

        embed.set_footer(text='Programación competitiva')

        await message.channel.send(embed=embed)

    if message.content.startswith('$fecha'):
        COL = pytz.timezone('America/Bogota')
        today = datetime.now(tz=COL)
        res = today.strftime("%d/%m/%Y %H:%M:%S")
        await message.channel.send(">>> La fecha y hora actual es: " +
                                   str(res))

    if message.content.startswith('$test'):
        miConexion = pymysql.connect(
            host='freedb.tech',
            user='freedbtech_main',
            passwd='ecciccpl2015',
            db='freedbtech_artemis')
        cur = miConexion.cursor()
        cur.execute(
            "SELECT tema,texto FROM temario where tema='Binary Search' ")
        for i in cur.fetchall():
            lista = list(i)

            notag = re.sub("<.*?>", " ", lista[1])
            #### Create the initial embed object ####
            embed = discord.Embed(
                title=lista[0], description=notag, color=242424)
            lista[0] = lista[0].replace(' ', '%20')
            # set author
            embed.set_author(
                name='Guia del programador competitivo',
                icon_url=
                'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
            )

            url2 = 'https://res.cloudinary.com/dw0butj4g/image/upload/v1611352499/' + str(
                lista[0]) + '.png'

            print(url2)
            # set image
            embed.set_image(url=url2)

            # set thumbnail
            embed.set_thumbnail(
                url=
                'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348303/gpc_nhaobw.jpg'
            )

            # set footer
            embed.set_footer(text='Diego Rodriguez')
            miConexion.close()
        await message.channel.send(embed=embed)

    if message.content.startswith('$listatemas'):
        page = int(message.content[12:])-1
        print (page)
        if page==0:
          miConexion = pymysql.connect(
              host='freedb.tech',
              user='freedbtech_main',
              passwd='ecciccpl2015',
              db='freedbtech_artemis')
          cur = miConexion.cursor()
          cur.execute(
              "SELECT tema FROM temario  where id<100 ORDER BY id limit 100 ")
          aux = ""
          for i in cur.fetchall():
              lista = list(i)
              aux += str(lista[0]) + "\n"
          embed = discord.Embed(
              title="Lista de temas ***pagina 1 de 5*** ", description=aux, color=242424)
          # set author
          embed.set_author(
              name='Guia del programador competitivo',
              icon_url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
          )
          # set thumbnail
          embed.set_thumbnail(
              url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348303/gpc_nhaobw.jpg'
          )
          # set footer
          embed.set_footer(
              text='Programación competitiva',
              icon_url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
          )
          miConexion.close()
          await message.channel.send(embed=embed)
        elif page==1:
          miConexion = pymysql.connect(
              host='freedb.tech',
              user='freedbtech_main',
              passwd='ecciccpl2015',
              db='freedbtech_artemis')
          cur = miConexion.cursor()
          cur.execute(
              "SELECT tema FROM temario  where id between 100 and 150  ORDER BY id limit 100"
          )
          aux = ""
          for i in cur.fetchall():
              lista = list(i)
              aux += str(lista[0]) + "\n"
          embed = discord.Embed(
              title="Lista de temas ***pagina 2 de 5*** ", description=aux, color=242424)
          # set author
          embed.set_author(
              name='Guia del programador competitivo',
              icon_url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
          )
          # set thumbnail
          embed.set_thumbnail(
              url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348303/gpc_nhaobw.jpg'
          )
          # set footer
          embed.set_footer(
              text='Programación competitiva',
              icon_url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
          )
          miConexion.close()
          await message.channel.send(embed=embed)
        elif page==2:
          miConexion = pymysql.connect(
              host='freedb.tech',
              user='freedbtech_main',
              passwd='ecciccpl2015',
              db='freedbtech_artemis')
          cur = miConexion.cursor()
          cur.execute(
              "SELECT tema FROM temario  where id between 150 and 200  ORDER BY id limit 100"
          )
          aux = ""
          for i in cur.fetchall():
              lista = list(i)
              aux += str(lista[0]) + "\n"
          embed = discord.Embed(
              title="Lista de temas ***pagina 3 de 5*** ", description=aux, color=242424)
          # set author
          embed.set_author(
              name='Guia del programador competitivo',
              icon_url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
          )
          # set thumbnail
          embed.set_thumbnail(
              url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348303/gpc_nhaobw.jpg'
          )
          # set footer
          embed.set_footer(
              text='Programación competitiva',
              icon_url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
          )
          miConexion.close()
          await message.channel.send(embed=embed)
        if page==3:
          miConexion = pymysql.connect(
              host='freedb.tech',
              user='freedbtech_main',
              passwd='ecciccpl2015',
              db='freedbtech_artemis')
          cur = miConexion.cursor()
          cur.execute(
              "SELECT tema FROM temario  where id between 200 and 250  ORDER BY id limit 100"
          )
          aux = ""
          for i in cur.fetchall():
              lista = list(i)
              aux += str(lista[0]) + "\n"
          embed = discord.Embed(
              title="Lista de temas ***pagina 4 de 5*** ", description=aux, color=242424)
          # set author
          embed.set_author(
              name='Guia del programador competitivo',
              icon_url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
          )
          # set thumbnail
          embed.set_thumbnail(
              url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348303/gpc_nhaobw.jpg'
          )
          # set footer
          embed.set_footer(
              text='Programación competitiva',
              icon_url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
          )
          miConexion.close()
          await message.channel.send(embed=embed)
        if page==4:
          miConexion = pymysql.connect(
              host='freedb.tech',
              user='freedbtech_main',
              passwd='ecciccpl2015',
              db='freedbtech_artemis')
          cur = miConexion.cursor()
          cur.execute(
              "SELECT tema FROM temario  where id> 250  ORDER BY id limit 100")
          aux = ""
          for i in cur.fetchall():
              lista = list(i)
              aux += str(lista[0]) + "\n"
          embed = discord.Embed(
              title="Lista de temas ***pagina 5 de 5*** ", description=aux, color=242424)
          # set author
          embed.set_author(
              name='Guia del programador competitivo',
              icon_url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
          )
          # set thumbnail
          embed.set_thumbnail(
              url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348303/gpc_nhaobw.jpg'
          )
          # set footer
          embed.set_footer(
              text='Programación competitiva',
              icon_url=
              'https://res.cloudinary.com/dw0butj4g/image/upload/v1611348195/pp_hl1xgr.jpg'
          )
          miConexion.close()
          await message.channel.send(embed=embed)
    



keep_alive()
client.run(os.getenv('TOKEN'))
