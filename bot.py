from pyrogram import Client, filters
from pyrogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from os.path import exists
from json import loads,dumps 
from pathlib import Path
from os import listdir
from os import mkdir
from os import unlink
from os.path import isfile, join
from datetime import timedelta
from random import randint
import re
from re import findall
from bs4 import BeautifulSoup
from py7zr import FILTER_COPY
from multivolumefile import MultiVolume
from io import BufferedReader
from py7zr import SevenZipFile
from move_profile import move_to_profile
from urllib.parse import quote
from time import time, localtime
from yarl import URL
import asyncio
import tgcrypto
import aiohttp_socks
import aiohttp
import requests
import traceback
import time
import os
import ssl
import http.server
import socketserver
import yt_dlp
from uptodl import search, get_info
import psutil

ssl._create_default_https_context = ssl._create_unverified_context


def sevenzip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size

    if not volume:
        volume = fsize + 1024

    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3

    with MultiVolume(
        fpath.with_name(fpath.name + ".7z"), mode="wb", volume=volume, ext_digits=ext_digits
    ) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)

            archive_writer.write(fpath, fpath.name)

    files = []
    for file in archive._files:
        files.append(file.name)
    unlink(fpath)
    return files
	
	

from configs import api_id, api_hash, token
admins = ['migue_2010']
bot = Client("client",api_id,api_hash,bot_token=token) 
CONFIG = {}
global_conf = {
       "token": "f5dcd525ee12d5552dc4cfb405b324e7",
       "host": "https://cursos.uo.edu.cu/"
   }
   
url_temp = {"Actual_url":""}
   
automatic = {"status":"on"}  

traffic = {
"downlink":"0",
"uplink":"0"}

traffico = 0

print(global_conf["host"])


stream_sites = ['youtube.com', 'xnxx.com', 'twitch.tv', 'dailymotion.com']



SECOND = 0


def getuser(username):
    try:
        user_info = CONFIG[username]
        return user_info
    except:
        return None

def createuser(username):
    CONFIG[username] = {"username":"","password":"","proxy":"","zips":"","calidad":"None"}
	
	
def deleteuser(username):
    
    if username in CONFIG:
        del CONFIG[username]
        print(f"Usuario {username} eliminado de la configuración.")
    else:
        print(f"El usuario {username} no existe en la configuración.")


	
@bot.on_message()
async def new_event(client: Client, message: Message):
    global traffico
    await bot.set_bot_commands([
            BotCommand("start","Inicia bot"),
            BotCommand("zips","Configura el tamaño de los zips"),
            BotCommand("add","Añade usuarios Solo admin"),
            BotCommand("ban","elimina usuario Solo admin"),
            BotCommand("calidad","Configura calidad de videos"),
            BotCommand("addsite","Añade sitios para descarga de stream"),
			BotCommand("config","COnfigura token"),
			BotCommand("auto","Configurar las subidas automaticas"),
			BotCommand("ls","Ver archivos en el bot"),
			BotCommand("rm","Borrar archivos en el bot"),
			BotCommand("rename","Renombrar archivos"),
			BotCommand("status","Muestra datos del sistema"),
			BotCommand("delall","Borra todos los archivos"),
			BotCommand("help","ayuda basica")])
			
    msg = message.text
    id = message.from_user.id
    username = message.from_user.username
    @bot.on_callback_query(filters.regex(r"^/download"))
    async def download_callback(client, query):
        url = url_temp["Actual_url"]  # Obtén la URL almacenada en el diccionario
    # Llama a la función download_file() con los parámetros necesarios
        await download_file(url, id, query.message, callback=download_func)  # Usa query.message para el mensaje
        await query.answer("Descargando archivo...")
    if msg is None:
        msg = ""
    
    if getuser(username):
        if exists(str(id)):
            pass
        else:
            mkdir(str(id))
        pass
    else:
        if username in admins:
            createuser(username)
        else:
            await bot.send_message(id,f"⭕️**@{username} no tienes acceso a este bot.**")
            return
    if "/start" in msg:
        await message.reply(f"🤝Bienvenido @{username}. **Este bot es capaz de subir a la nube ")
		
    elif "/calidad" in msg:
        calidad = msg.split(" ")[1]
        CONFIG[username]["calidad"] = calidad
        await bot.send_message(id, "Se a actualizado la preferencia de calidad")
	    
    elif "/zips" in msg:
        zips = msg.split(" ")[1]
        CONFIG[username]["zips"] = zips
        await bot.send_message(id,"📚**Se guardo correctamente el tamaño de los zips.**")
		
    elif "/addadmin" in msg:
        admin = msg.split()[1]
		
        if admin in admins:
            await bot.send_message(id, "El usuario ya es admin")
        else:
            admins.append(admin)
            await bot.send_message(id, f"Ahora {admin} es admin del bot")
			
    elif "/addsite" in msg:
        site = msg.split()[1]
		
        if site in stream_sites:
            await bot.send_message(id, "Ya estan habilitadas las descargas de ese sitio")
        else:
            stream_sites.append(site)
            await bot.send_message(id, f"Ahora el bot tambien descargara de {site} ")
			
    elif "/removeadmin" in msg:
        admin = msg.split()[1]

        if admin in admins:
            admins.remove(admin)
            deleteuser(username)
            await bot.send_message(id, f"Se eliminó a {admin} como admin del bot.")
        else:
            await bot.send_message(id, f"El usuario {admin} no es admin del bot.")

	
    elif "/proxy" in msg:
        zips = msg.split(" ")[1]
        proxy = iprox(zips.replace("socks5://",""))
        CONFIG[username]["proxy"] = f"socks5://{proxy}"
        await bot.send_message(id,"📡**Se guardo correctamente el proxy.**")
    
    elif "/offproxy" in msg:
        CONFIG[username]["proxy"] = ""
        await bot.send_message(id,"📡**Se elimino correctamente el proxy.**")
    
    elif "/add" in msg:
        if username in admins:  
            usernames = msg.split(" ")[1]  
            createuser(usernames)  
            await bot.send_message(id, f"✅@{usernames} fue añadido al bot.")
        else:
           await bot.send_message(id, "❌No puedes usar este comando. Es solo para administradores.")
           return

    elif "/ban" in msg:
        if username in admins:  
            usernames = msg.split(" ")[1]  
            deleteuser(usernames)  
            await bot.send_message(id, f"✅ @{usernames} fue eliminado del bot.")
        else:
            await bot.send_message(id, "❌ No puedes usar este comando. Es solo para administradores.")
            return


		
	    
			
    elif "/auto" in msg:
        try:
            if automatic["status"] == "on":
                automatic["status"] = "on"
                await bot.send_message(id, "Subidas automaticas activadas.")
            else:
                automatic["status"] = "off"
                await bot.send_message(id, "Subida automatica desactivada")
        except Exception as e:
            await bot.send_message(id, f"Error al cambiar el modo automático: {e}")			
			
			
			
	
    elif "/config" in msg:
        parts = msg.split(" ", 2)  
        if len(parts) == 3:
            _, host, token = parts  

        
            global_conf["host"] = host
            global_conf["token"] = token 

            await bot.send_message(id, f"Configuración almacenada correctamente: \n Host: {host}\n Token: {token}")
        else:
            await bot.send_message(id, "Error al guardar la configuración. Formato correcto: /config host token")

    elif "/up" in msg:
        try:
        
            parts = msg.split()  
            if len(parts) >= 2:
                index = int(parts[1])  

                count = 0
                directory = os.path.join(str(id))
                if os.path.exists(directory):
                    for item in listdir(directory):
                        if isfile(join(directory, item)):
                            if count == index:
                                filename = item  # Obtener el nombre del archivo
                                msg = await bot.send_message(id, "Comenzando a subir")
                                await uploadfile(f"{id}/{filename}", msg, username)
                                
                                return  # Termina la ejecución del comando
                            count += 1
                    await bot.send_message(id, f"Índice {index} no encontrado.") 
                else:
                    await bot.send_message(id, f"La ruta {directory} no existe.") 
            else:
                await bot.send_message(id, "Uso incorrecto del comando. Usa /up <índice>")
        except (IndexError, ValueError):
            await bot.send_message(id, "Uso incorrecto del comando. Usa /up <índice>")
        except Exception as e:
            await bot.send_message(id, f"Error al subir el archivo: {e}")			
			


    elif "/rename" in msg:
        try:
        # Obtener el índice y el nuevo nombre del archivo
            parts = msg.split()
            if len(parts) >= 3:
                index = int(parts[1])
                new_filename = parts[2]

                count = 0
                directory = os.path.join(str(id))
                if os.path.exists(directory):
                    for item in listdir(directory):
                        if isfile(join(directory, item)):
                            if count == index:
                                old_filename = item
                                old_path = join(directory, old_filename)
                                new_path = join(directory, new_filename)

                            # Renombrar el archivo
                                os.rename(old_path, new_path)

                                await bot.send_message(id, f"Archivo {old_filename} renombrado a {new_filename}.")
                                return  # Termina la ejecución del comando
                            count += 1
                    await bot.send_message(id, f"Índice {index} no encontrado.")
                else:
                   await bot.send_message(id, f"La ruta {directory} no existe.")
            else:
                await bot.send_message(id, "Uso incorrecto del comando. Usa /rename <índice> <nuevo_nombre>")
        except (IndexError, ValueError):
            await bot.send_message(id, "Uso incorrecto del comando. Usa /rename <índice> <nuevo_nombre>")
        except Exception as e:
            await bot.send_message(id, f"Error al renombrar el archivo: {e}")

			
			
    elif "/rm" in msg:
        try:
            parts = msg.split()
            index = int(parts[1])  # Obtiene el índice del archivo a borrar

            count = 0
            directory = os.path.join(str(id))  # Crea la ruta completa
            if os.path.exists(directory):
                for item in listdir(directory):
                    if isfile(join(directory, item)):
                        if count == index:
                            file_to_delete = join(directory, item)
                            os.remove(file_to_delete)
                            await bot.send_message(id, f"Archivo {item} eliminado correctamente.")
                            return  # Termina la ejecución del comando
                        count += 1
                await bot.send_message(id, f"Índice {index} no encontrado.") 
            else:
                await bot.send_message(id, f"La ruta {directory} no existe.") 
        except (IndexError, ValueError):
            await bot.send_message(id, "Uso incorrecto del comando. Usa /rm <índice>")

    elif "/delall" in msg:
        try:
            directory = os.path.join(str(id))  # Crea la ruta completa
            if os.path.exists(directory):
                for item in listdir(directory):
                    if isfile(join(directory, item)):
                        file_to_delete = join(directory, item)
                        os.remove(file_to_delete)
                await bot.send_message(id, "Todos los archivos han sido eliminados.")
            else:
                await bot.send_message(id, f"La ruta {directory} no existe.") 
        except Exception as e:
            await bot.send_message(id, f"Error al eliminar archivos: {e}")			
			
    elif "/help" in msg:
        msg = "Bienvenido Soy un bot que descarga y sube a la nube\n\n"	
        msg += "Primer paso para poder usarme es configurar /zips 99\n"
        msg += "Seundo paso para usarme es configurar el token usando /config\n"
        msg += "Tercer paso para usarme es configurar calidad de videos /calidad 480p\n"
        msg += "Cuarto paso si deseas editar el archivo antes de subirlo puedes usar /ls y luego /rename respectivamente\n"
        msg += "SI no deseas cambiar nombre del archivo y deseas que este proceso de subida sea automatico usa /auto\n"
        msg += "Gracias por usarme"
        await bot.send_message(id,msg)
		
    elif "/ls" in msg:
        count = 0
        msg = ""
        directory = os.path.join(str(id))#Acceder a la carpeta del usuario
        if os.path.exists(directory):
            for item in listdir(directory):
            
                if isfile(join(directory, item)): #Buscar los archivos
                     msg += f"{count} - {item}\n"
                     count += 1
            await bot.send_message(id, msg)
        else:
            await bot.send_message(id, f"La ruta {directory} no existe.")
			
    elif "/search" in msg:
        parts = msg.split(" ")
        if len(parts) == 3:
            tag = parts[1]
            name = parts[2]
            results = search(name=name, tag=tag)
            item = results[0]
            info = get_info(item, include_down_url=True)
            name = info["name"]
            text = info["text"]
            url = info["url"]
            url_temp["Actual_url"] = url
            msg = f"📃Nombre: {name}\n"
            msg += f"📜Descripcion: {text}\n\n"
            msg += f"🔗Link: {url}"
        
            @Client.on_callback_query(filters.regex(r"^/download"))
            async def download_callback(client, query):
                url = query.data.split(" ")[1]  # Obtén la URL del callback_data
    # Llama a la función download_file() con los parámetros necesarios
                await download_file(url, id, query.message, callback=download_func)  # Usa query.message para el mensaje
                await query.answer("Descargando archivo...")  # Envía una respuesta al usuario 
		

        # Crea un botón con el comando "/download"
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Descargar", callback_data="/download")]])

        # Envía el mensaje con el botón
            msg = await bot.send_message(id, msg, reply_markup=keyboard)
        else:	
            await bot.send_message(id, "Error Debe poner /search android Telegram")
	
    elif message.video or message.audio or message.photo or message.document or message.sticker or message.animation:
        try:
            filename = str(message).split('"file_name": ')[1].split(",")[0].replace('"',"")
            filesize = int(str(message).split('"file_size":')[1].split(",")[0])
        except:
            filename = str(randint(11111,99999))
        msg = await bot.send_message(id,"⬇️Descargando...")
        start = time.time()
        path = await message.download(file_name=f"{id}/{filename}",progress=download_func,progress_args=(filename,start,msg))
        traffico += filesize  
        await msg.edit("✅Archivo descargado.")

    # Comprueba si el modo automático está activado
        if automatic["status"] == "on":
            await uploadfile(f"{id}/{filename}", msg, username)
 
    elif "https" in msg and not "www.mediafire.com" and not any(site in msg for site in stream_sites):
        url = msg.split(" ")[0]
        msg = await bot.send_message(id, "⬇️Descagrando")
        filename = await download_file(url, id, msg, callback=download_func)
        if filename:
            await msg.edit("Descargado correctamente")
            
            if automatic["status"] == "on":
                await uploadfile(f"{id}/{filename}", msg, username)
        
        

    elif "https://www.mediafire.com/" in msg:
        print("Descargando de MediaFire")
    
        url = msg.split(" ")[0]
        msg = await bot.send_message(id, "Descargando de MediaFire")
        filename = await download_mediafire(url, id, msg, callback=download_func)
        if filename:
            msg.edit(f"Se a descargado el archivo {filename} compruebe usando /ls")
        
        # Comprueba si el modo automático está activado
            if automatic["status"] == "on":
                await uploadfile(f"{id}/{filename}", msg, username)
                await bot.send_message(id, "Archivo subido automáticamente.")
      
    elif any(site in msg for site in stream_sites):
        url = msg.split(" ")[0]
        msg = await bot.send_message(id, "⬇️ Descargando...")
        quality = CONFIG[username]["calidad"]
        if "None" in quality:
            await bot.send_message(id, "Porfavor configura la calidad a descargar. Ejemplo /calidad 480p")
        else:
            filename = await ytdlp_downloader(url, id, msg, username, lambda data: download_progres(data,msg,format,username), quality)
            ip = obtener_ip_publica()
            print(ip)	
            if filename:
                await msg.edit(f"Se a descargado el archivo {filename} use el comando /ls")
            
            # Comprueba si el modo automático está activado
                if automatic["status"] == "on":
                    await uploadfile(filename, msg, username)
                    
                
            else:
                await bot.send_message("No se a completado la descarga vuelva a intentarlo")

			

			
    elif "/status" in msg:
        system_info = await get_system_info()        	
        cpu = system_info['cpu_percent']
        ram = system_info['ram_total']
        ram_used = system_info['ram_used']
        ram_percent = system_info['ram_percent']
        ram_free = system_info['ram_free']
        Disk = system_info['disk_total']
        Disk_used = system_info['disk_used']
        Disk_free = system_info['disk_free']
        downlink = traffic["downlink"]
        uplink = traffic["uplink"]
        traffics = sizeof_fmt(traffico)
        msg = "🎛Datos del Sistema\n\n"
        msg += f"💻CPU: {cpu}%\n"
        msg += f"💽Ram: {ram}\n"
        msg += f"🎚Uso de Ram: {ram_used}\n"
        msg += f"🖱Ram disponible: {ram_free}\n"
        msg += f"🗜Porcentaje Ram: {ram_percent}%\n"
        msg += f"💿Disco total: {Disk}\n"
        msg += f"📀Disco Usado: {Disk_used}\n"
        msg += f"🧭Disco Libre: {Disk_free}\n"
        msg += "⚡️Trafico de red\n\n"
        msg += f"🔽Descarga: {downlink}/s\n"
        msg += f"🔼Subida: {uplink}/s\n\n"
        msg += f"Trafico total: {traffics}"
        await bot.send_message(id,msg)
		
		
                
			
async def download_func(current, total, filename, starttime, msg):
    """Muestra el progreso de la descarga."""
    speed = time.time() - starttime  
    if speed > 0:  
        speed = current / speed
    else:
        speed = 0  
    percentage = int((current / total) * 100)

    message = "⬇️ Descargando archivo...*\n"
    message += f"⬇️ *Descargado: {sizeof_fmt(current)}\n"
    message += f"🗂 Total: {sizeof_fmt(total)}\n"
    message += f"🚀 Velocidad: {sizeof_fmt(speed)}\n"
    message += f"⏳ Porcentaje: {percentage}%\n"
    traffic["downlink"] = sizeof_fmt(speed)

    global SECOND
    # Call localtime from the time module
    if SECOND != localtime().tm_sec: 
        try:
            await msg.edit(message)
        except Exception as ex:
            print(ex)
            pass
    SECOND = localtime().tm_sec


	
	
def upload_func(current,total,starttime,filename,msg):
    speed = time.time() - starttime  
    if speed > 0:  
        speed = current / speed
    else:
        speed = 0  
    percentage = int((current / total) * 100)

    message = "⬇️ Subiendo*\n"
    message += f"⬇️ *Subido: {sizeof_fmt(current)}\n"
    message += f"🗂 Total: {sizeof_fmt(total)}\n"
    message += f"🚀 Velocidad: {sizeof_fmt(speed)}\n"
    message += f"⏳ Porcentaje: {percentage}%\n"
    traffic["uplink"] = sizeof_fmt(speed)

    global SECOND
    # Call localtime from the time module
    if SECOND != localtime().tm_sec: 
        try:
            msg.edit(message)
        except Exception as ex:
            print(ex)
            pass
    SECOND = localtime().tm_sec


class UploadProgress(BufferedReader):
    def __init__(self,file,callback):
        f = open(file, "rb")
        self.filename = file.split("/")[-1]
        self.__read_callback = callback
        super().__init__(raw=f)
        self.start = time.time()
        self.length = os.path.getsize(file)
    
    def read(self, size=None):
        calc_sz = size
        if not calc_sz:
            calc_sz = self.length - self.tell()
        self.__read_callback(self.tell(), self.length,self.start,self.filename)
        return super(UploadProgress, self).read(size)
        
async def uploadfile(file, msg, username):
    global global_conf
    
    original_filename = os.path.basename(file)  # Obtiene el nombre de archivo de la ruta original
    fsize = Path(file).stat().st_size
    zips_size = 1024 * 1024 * int(CONFIG[username]["zips"])


    path = [file]
    if fsize > zips_size:
        await msg.edit("📚Comprimiendo...")
        path = sevenzip(file, volume=zips_size)

    try:
        if CONFIG[username]["proxy"] == "":
            connector_on = aiohttp.TCPConnector()
        else:
            connector_on = aiohttp_socks.ProxyConnector.from_url(CONFIG[username]["proxy"])
        async with aiohttp.ClientSession(connector=connector_on) as session:
            token = global_conf["token"]
            
            urls = []
            if token:
                for fpath in path:
                    await msg.edit(f"⬆️Subiendo...")
                    file = UploadProgress(
                        fpath,
                        lambda current, total, start, filename: upload_func(
                            current, total, start, filename, msg
                        ),
                    )
                    upload = await uploadtoken(file, token, session)
                    if upload:
                        url = upload
                        await msg.edit(
                            "✅Subida completada. Procediendo a convertir el link a perfil..."
                        )

                        if url:
                            url = url.replace("draftfile.php/", "webservice/draftfile.php/")
                            url = url + "?token=" + token
                            urls.append(url)
                            await msg.edit(f"✅Subida exitosa")

                # Mover la lógica de escritura del archivo fuera del bucle for
                print(urls)
                if urls:
                    with open(f"{original_filename}.txt", "w") as txt:  # Usa original_filename
                        txt.write("\n".join(urls))
                    await bot.send_document(username, f"{original_filename}.txt")
                    os.remove(f"{original_filename}.txt")
                else:
                    await msg.edit(f"❌ No se pudo subir ningún archivo.")
            else:
                await bot.send_message(
                    username,
                    "⭕️No se completo el inicio de seccion posibles razones: web caida , token incorrecto, token baneado",
                )
                return
    except Exception as ex:
        traceback.print_exc()
        await bot.send_message(username, f"{ex}")


async def uploadtoken(f, token, session):
    try:
        # Declara global_conf como global
        global global_conf

        # Obtén el host desde el diccionario
        host = global_conf["host"]
        
        

        url = f"{host}webservice/upload.php"
        query = {"token": token, "file": f}
        async with session.post(url, data=query, ssl=True) as response:
            text = await response.text()
            print(text)
            dat = loads(text)[0]
            url = f"{host}draftfile.php/{str(dat['contextid'])}/user/draft/{str(dat['itemid'])}/{str(quote(dat['filename']))}"
            return url
    except:
        traceback.print_exc()
        return None

import yt_dlp
import aiohttp
import time

def download_progres(data,message,format, username):
    global CONFIG
    quality = CONFIG[username]["calidad"]
    if data["status"] == "downloading":
        filename = data["filename"].split("/")[-1]
        _downloaded_bytes_str = data["_downloaded_bytes_str"]
        _total_bytes_str = data["_total_bytes_str"]
        if _total_bytes_str == "N/A":
            _total_bytes_str = data["_total_bytes_estimate_str"]        
        _speed_str = data["_speed_str"].replace(" ","")
        _eta_str = data["_eta_str"]
        _format_str = format        
        msg= f"{filename}\n"
        msg+= f"💾Descargado: {_downloaded_bytes_str}\n"
        msg+= f"📦Total: {_total_bytes_str} \n"
        msg+= f"⚡️Velocidad: {_speed_str}/s \n"
        msg+= f"🎥Calidad: {quality}\n"
        msg+= f"⏰Tiempo restante: {_eta_str}"
        traffic["downlink"] = _speed_str
        global SECOND 
        if SECOND != localtime().tm_sec:
        #if int(localtime().tm_sec) % 2 == 0 :
            try:
                message.edit(msg,reply_markup=message.reply_markup)
            except:
                pass
        SECOND = localtime().tm_sec

		
		
async def ytdlp_downloader(url, id, msg, username, callback, format):
    """Descarga un video de YouTube utilizando yt-dlp."""

    class YT_DLP_LOGGER(object):
        def debug(self, msg):
            pass
        def warning(self, msg):
            pass
        def error(self, msg):
            pass

    resolution = str(format)
    dlp = {
        "logger": YT_DLP_LOGGER(),
        "progress_hooks":[callback],
        "outtmpl": f"{id}/%(title)s.%(ext)s",
        "format": f"best[height<={resolution}]"
    }

    downloader = yt_dlp.YoutubeDL(dlp)
    print("Se esta descargando mamawebo")
    loop = asyncio.get_running_loop()

    # Obtén información sobre el video
    filedata = await loop.run_in_executor(None, downloader.extract_info, url)

    # Verifica si la descarga está dividida
    if "entries" in filedata:
        # Descarga dividida
        total_size = 0
        for entry in filedata["entries"]:
            total_size += entry["filesize"]
    else:
        # Descarga completa
        if "filesize" in filedata:
            total_size = filedata["filesize"]
        else:
            # No se puede obtener el tamaño total
            total_size = 0

    # ... (tu código para el progreso de la descarga)
    filepath = downloader.prepare_filename(filedata)
    filename = filedata["requested_downloads"][0]["_filename"]
    return filename

def obtener_ip_publica():
  """Obtiene la IP pública usando la API de icanhazip.com."""
  try:
    response = requests.get("https://icanhazip.com/")
    return response.text.strip()
  except requests.exceptions.RequestException as e:
    print(f"Error al obtener la IP: {e}")
    return None	
	
	
	
	

async def extractDownloadLink(contents):
    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]	
	

import asyncio
import aiohttp
import certifi
import ssl	


async def download_file(url, id, msg, callback=None):
    global traffico
    """Downloads a file from MediaFire and saves it to a specified path."""

    # Create a context object
    context = ssl.create_default_context(cafile=certifi.where())  

    # Use the ssl parameter with the context object
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            ssl=context  # Use the SSL context directly 
        )
    ) as session:
        response = await session.get(url)

        response = await session.get(url)
        filename = url.split("/")[-1]

        # Save to {id}/{filename} 
        path = f"{id}/{filename}"
        f = open(path, "wb")

        chunk_ = 0
        total = int(response.headers.get("Content-Length"))
        traffico += total
        start = time.time()  # Llama a la función time.time() para obtener el tiempo actual
        while True:
            chunk = await response.content.read(1024)
            if not chunk:
                break
            chunk_ += len(chunk)
            if callback:
                await callback(chunk_, total, filename, start, msg)
            f.write(chunk)
            f.flush()

        return path

@Client.on_callback_query(filters.regex(r"^download_"))  # Filtra por el prefijo "download_"
async def download_callback(client, query):
    global url_temp
    url = url_temp["Actual_url"]
    await download_file(url, id, query.message, callback=download_func)
    await query.answer("Descargando archivo...")		
		
		


	
async def download_mediafire(url, id, msg, callback=None):
    """Downloads a file from MediaFire and saves it to a specified path."""
    global traffico

    # Create a context object
    context = ssl.create_default_context(cafile=certifi.where())  

    # Use the `ssl` parameter with the context object
    session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            ssl=context  # Use the SSL context directly 
        )
    )
    
    response = await session.get(url)
    url = await extractDownloadLink(await response.text())
    response = await session.get(url)
    filename = response.content_disposition.filename

    # Save to {id}/{filename} 
    path = f"{id}/{filename}"
    f = open(path, "wb")

    chunk_ = 0
    total = int(response.headers.get("Content-Length"))
    traffico += total
    start = time.time()
    while True:
        chunk = await response.content.read(1024)
        if not chunk:
            break
        chunk_ += len(chunk)
        if callback:
            await callback(chunk_, total, filename, start, msg)
        f.write(chunk)
        f.flush()

    return path

	
        
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Yi', suffix)

async def get_cpu_percent():
    """Obtiene el porcentaje de uso de la CPU en un hilo separado."""
    loop = asyncio.get_event_loop()
    cpu_percent = await loop.run_in_executor(executor, psutil.cpu_percent)  # No se necesita el argumento 'interval'
    return cpu_percent

import asyncio
import psutil
import os
import time
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()
	
	
	
	
async def get_system_info():
    """Obtiene información del sistema y la devuelve como un diccionario."""
    
    info = {}

    # Memoria RAM
    ram = psutil.virtual_memory()
    info["ram_total"] = sizeof_fmt(ram.total)
    info["ram_used"] = sizeof_fmt(ram.used)
    info["ram_free"] = sizeof_fmt(ram.free)
    info["ram_percent"] = ram.percent

    # CPU
    info["cpu_percent"] = await get_cpu_percent()

    # Almacenamiento del disco
    disk = psutil.disk_usage('/')  # Obtener información del disco raíz ('/')
    info["disk_total"] = sizeof_fmt(disk.total)  # Convertir a GB
    info["disk_used"] = sizeof_fmt(disk.used)  # Convertir a GB
    info["disk_free"] = sizeof_fmt(disk.free)  # Convertir a GB
    info["disk_percent"] = disk.percent

    return info
   
	
	
	
	
	
def iprox(proxy):
    tr = str.maketrans(
        "@./=#$%&:,;_-|0123456789abcd3fghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBAzyIwvutsrqponmlkjihgf3dcba9876543210|-_;,:&%$#=/.@",
    )
    return str.translate(proxy[::2], tr)
	
	
import threading
import http.server
import socketserver
# Asegúrate de importar tu módulo bot

# Función para ejecutar el servidor web
def run_server():
    PORT = 9000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# Función para ejecutar el bot
def run_bot():
    bot.run()  # Suponiendo que 'run()' es la función que inicia tu bot

if __name__ == "__main__":
    # Inicia el servidor web en un hilo separado
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Ejecuta el bot en el hilo principal
    run_bot() 





