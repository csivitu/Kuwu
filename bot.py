#import json
import discord
from discord.ext import commands, tasks
import os, socket
from dotenv import load_dotenv
import threading, time
from asgiref.sync import async_to_sync
from flask import Flask, request
load_dotenv()

app = Flask(__name__)

global monitor_data
monitor_data = {}

global tags
tags = []

global challenges
challenges = {'pwn-intended-0x1':30001, 'pwn-intended-0x2':30007, 'pwn-intended-0x3':30013, 'Global Warming':30023, 'Cascade':30203,
              'CCC':30215, 'File Library':30222, 'Mr Rami':30231, 'Oreo':30243, 'The Confused Deputy':30256, 'Warm Up':30272, 'Secure Portal':30281 }

global connectionData
connectionData = {}

@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        c={}
        c['client_addr']=request.environ['REMOTE_ADDR']
#       req_data = request.get_json()
        data = str(request.form['stats']).split(',')
        l = len(data)
        i = 4
        while (i<l):
            c[data[i].strip()]=data[i+1:i+4]
            i+=4
        global monitor_data
        monitor_data = c
        global tags
        t = str(request.form['ids']).split(',')
        for j in t:
            tags.append(j.strip())
        print('data has been recieved!')
        return "data recieved!"
    return "Hello Test!"

@app.route('/firstBlood', methods=['POST','GET'])
def get_first_blood():
    if request.method == 'POST':
        name = str(request.form['playerName'])
        challengeName = str(request.form['challengeName'])
        res = firstBlood(name,challengeName)
        return res
    else:
        return "Hello world!"

def run_server():
    if __name__ == '__main__':
        app.run(host=os.getenv('HOST'),port=os.getenv('PORT'))

t1  = threading.Thread(target=run_server)
t1.start()

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    # monitorChallenges.start()
    # challengeStatus.start()
    checkChallenges.start()
    await client.change_presence(status =  discord.Status.online, activity=discord.Game('Type .list to list all commands'))
    print('Bot is ready')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@tasks.loop(seconds = 60)
async def challengeStatus():

    print('testing')
    statusChannel = client.get_channel(int(os.getenv('CHALLENGE_STATUS_CHANNEL')))
    w = ''
    table = [['TAGS','CONTAINER ID','Name', 'CPU %', 'MEM%']]

    if monitor_data == {}:
        return

    
    for i in dict.keys(monitor_data):
        
        if (i == 'client_addr'):
            continue
        
        print(tags[tags.index(i)-1])
        table.append([tags[tags.index(i)-1], i, monitor_data[i][0], monitor_data[i][1], monitor_data[i][2]])
    
    for row in table:
        w += "{: >20} {: >20} {: >20} {: >20} {: >20}".format(*row)+'\n'

    print('hello world!')

    clientIp = monitor_data['client_addr']
    w += f'\n\nData recieved from I.P {clientIp}'

    await statusChannel.send(w) #send challenge data here!
    print('Data sent!')


@tasks.loop(seconds = 15)
async def monitorChallenges():
    
    if(monitor_data == {}):
        return
    

    channel = client.get_channel(int(os.getenv('CHALLENGE_STATUS_CHANNEL')))

    print('not returned')

    for i in dict.keys(monitor_data):
        if (i == 'client_addr' or  i == 'CONTAINER'):
            continue

        if(float(monitor_data[i][1][0:-1]) > 50.00):
            await channel.send(f'{monitor_data[i][0]} has a CPU usage of {monitor_data[i][1]}.\n Please check. \nID: {i}')

        if (float(monitor_data[i][2][0:-1]) > 60.00):
            await channel.send(f'{monitor_data[i][0]} has a memory usage of {monitor_data[i][4]}\nPlease check.\nID: {i}')

            

@tasks.loop(seconds = 120)
async def checkChallenges():
    global connectionData
    connectionData={}
    server = socket.gethostbyname('ctf-chall-dev.csivit.com')
    ch = client.get_channel(int(os.getenv('CHALLENGE_STATUS_CHANNEL')))
    embed = discord.Embed(title="Challenge Status")
    for i in challenges:
        ADDR = (server, int(challenges[i]))
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            t1 = time.time()
            socket_client.connect(ADDR)
            t2 = time.time()
            t = str(t2-t1)
            t = t[0:t.index('.')+4]
            data = f'```css\nTime: {t}s```'
            embed.add_field(name=i,value=data)
            connectionData[i]=data
        except:
            data = f"```diff\n-Unable to connect.```"
            embed.add_field(name=i, value=data)
            connectionData[i]=data

    await ch.send(embed=embed)
    print('sent')

@client.command(aliases=['Challenges', 'challenges', 'challenge'])
async def challengeStats(ctx):
    if(not(len(connectionData) == len(challenges))):
        await ctx.send('Data is being collected, please wait for a few seconds!')
        return
    
    embed = discord.Embed(title='Challenge Status')
    for i in connectionData:
        embed.add_field(name=i, value=connectionData[i])
    
    await ctx.send(embed=embed)


@client.command(aliases=['Status', 'stats'])
async def status(ctx):

    if (monitor_data == {}):
        await ctx.send('There is no data to be sent!')
        return

    w = ''
    table = [['TAGS','CONTAINER ID','Name', 'CPU %', 'MEM%']]

    if monitor_data == {}:
        return

    
    for i in dict.keys(monitor_data):
        
        if (i == 'client_addr'):
            continue
        
        print(tags[tags.index(i)-1])
        table.append([tags[tags.index(i)-1], i, monitor_data[i][0], monitor_data[i][1], monitor_data[i][2]])
    
    for row in table:
        w += "{: >20} {: >20} {: >20} {: >20} {: >20}".format(*row)+'\n'

    clientIp = monitor_data['client_addr']
    w += f'\n\nData recieved from I.P {clientIp}'

    await ctx.send(w)
    print('Data sent')

@client.command(aliases=['Flag'])
async def flag(ctx):
    if ctx.channel.type is discord.ChannelType.private:
        await ctx.send(os.getenv('FLAG'))
    else:
        await ctx.channel.purge(limit=1)
        await ctx.send('Sssssshhh, not here. DM me maybe ;)')

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
        await ctx.send('Bot does not have permissions to perform the task. Please grant permissions')
    
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Bot does not have permissions to perform the task. Please give permission')

@async_to_sync
async def firstBlood(userName, challengeName):
    channel = client.get_channel(int(os.getenv('FIRST_BLOOD_CHANNEL')))
    await channel.send(f'{userName} got first blood in challenge: {challengeName}')
    return "Sent"
    


client.run(os.getenv('TOKEN'))

#https://discord.com/oauth2/authorize?client_id=723828224307757178&scope=bot
