import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import threading
import socket
import asyncio
load_dotenv()


PORT = int(os.getenv('PORT'))
SERVER  = socket.gethostbyname(socket.gethostname())
print(SERVER)
server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR  = (SERVER, PORT)
server.bind(ADDR)

def handleClient(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected')

    connected = True
    while connected:
        msg_lenght = conn.recv(64).decode('utf-8')
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = conn.recv(msg_lenght).decode('utf-8')
            if(msg == '!DISCONNECT'):
                connected = False
            print(f'[{addr}]: {msg}')
    
    conn.close()

def start():
    server.listen()
    print(f'Server is listening on port {PORT}')
    while True:
        conn, addr = server.accept()
        thread  = threading.Thread(target=handleClient, args= (conn, addr))
        thread.start()

t1  = threading.Thread(target=start)
t1.start()

print('program continues!')
client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    await client.change_presence(status =  discord.Status.online, activity=discord.Game('Type .list to list all commands'))
    print('Bot is ready')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

async def challengeStatus():
    await client.wait_until_ready()

    while not client.is_closed:
        statusChannel = client.get_channel(os.getenv('CHALLENGE_STATUS_CHANNEL'))
        await statusChannel.send('Status to be sent here!') #send challenge data here!
        asyncio.sleep(1800) #task will repeat every half an hour!

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('All required arguments not passed.')
        return
    
    if isinstance(error, commands.BadArgument):
        await ctx.send('Arguments sent not correct.')
        return
    
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command does not exist.')
        return

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('Bot does not have permissions to kick/ban people. Please grant permissions')
    
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Bot does not have permissions to perform the task. Please give permission')

async def firstBlood(userName, challengeName):
    channel = client.get_channel(os.getenv('FIRST_BLOOD_CHANNEL'))
    await channel.send(f'{userName} got first blood in challenge: {challengeName}')


if (os.getenv('MODE') == 'PRODUCTION'):
    client.loop.create_task(challengeStatus())


client.run(os.getenv('TOKEN'))

#https://discord.com/oauth2/authorize?client_id=723828224307757178&scope=bot