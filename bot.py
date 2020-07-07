#import json
import discord
from discord.ext import commands
import os, asyncio
from dotenv import load_dotenv
import threading, time
from flask import Flask, request
load_dotenv()

app = Flask(__name__)

data = []
challenges={}

@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        challenges={}
        challenges['client_addr']=request.environ['REMOTE_ADDR']
#       req_data = request.get_json()
        data = str(request.form['server']).split(',')
        l = len(data)
        i = 0
        while (i<l):
            challenges[data[i].strip()]=data[i+1:i+11]
            i+=11
        print(challenges)
        print('\n\n\n\n')
        return "data recieved!"
    return "Hello Test!"

def run_server():
    if __name__ == '__main__':
        app.run(host=os.getenv('HOST'),port=os.getenv('PORT'))

t1  = threading.Thread(target=run_server)
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
    if (challenges == {}):
        return

    statusChannel = client.get_channel(int(os.getenv('CHALLENGE_STATUS_CHANNEL')))
    w = ''
    table = [['Name', 'CPU %','MEM USAGE']]
    for i in dict.keys(challenges):
        if (i == 'client_addr'):
            continue
        iTable = []
        for j in range(4):
            iTable.append(challenges[i][j])
        table.append(iTable)
    
    for row in table:
        w += "{: >20} {: >20} {: >20}".format(*row)+'\n'

    clientIp = challenges['client_addr']
    w += f'\n\nData recieved from I.P {clientIp}'

    while True:
        await statusChannel.send(w) #send challenge data here!
        print(w)
        time.sleep(60) #updates will be sent every minute

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
    channel = client.get_channel(int(os.getenv('FIRST_BLOOD_CHANNEL')))
    await channel.send(f'{userName} got first blood in challenge: {challengeName}')

def creat_bg_task():
    print('task created!')
    client.loop.create_task(challengeStatus())

if (os.getenv('MODE') == 'PRODUCTION'):
    t2 = threading.Thread(target=creat_bg_task)
    t2.start()
    


client.run(os.getenv('TOKEN'))

#https://discord.com/oauth2/authorize?client_id=723828224307757178&scope=bot
