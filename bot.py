#import json
import discord
from discord.ext import commands, tasks
import os, socket
from dotenv import load_dotenv
import threading, time
from asgiref.sync import async_to_sync
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
load_dotenv()

app = Flask(__name__)

global monitor_data
monitor_data = {}

global tags
tags = []

global challenges
challenges = {'pwn-intended-0x1':30001, 'pwn-intended-0x2':30007, 'pwn-intended-0x3':30013, 'Global Warming':30023, 'Cascade':30203, 'find32':30630,
              'CCC':30215, 'File Library':30222, 'Mr Rami':30231, 'Oreo':30243, 'The Confused Deputy':30256,'The Usual Suspects':30279, 'Warm Up':30272, 'Secure Portal':30281,
              'Escape Plan':30419, 'Prison Break':30407, 'Blaise':30808, 'Vietnam':30814, 'AKA':30611, 'Where am I':30623, 'Login Error':30431, 'Body Count':30202,
              'Friends':30425, 'RicknMorty':30827, 'Secret Society': 30041, 'Smash':30046}

global ch
ch =  {13: {'name': 'Esrever', 'solved': False}, 14: {'name': 'Rivest_Shamir_Adleman', 'solved': False}, 15: {'name': 'Archenemy', 'solved': False}, 16: {'name': 'pwn_intended_0x2', 'solved': False}, 17: {'name': 'Blaise', 'solved': False}, 18: {'name': 'pwn_intended_0x1', 'solved': False}, 19: {'name': 'pwn_intended_0x3', 'solved': False}, 20: {'name': 'Prison_Break', 'solved': False}, 21: {'name': 'CCC', 'solved': False}, 22: {'name': 'File_Library', 'solved': False}, 24: {'name': 'The_Confused_Deputy', 'solved': False}, 25: {'name': 'Warm_Up', 'solved': False}, 26: {'name': 'Gradient_sky', 'solved': False}, 27: {'name': 'Mein_Kampf', 'solved': False}, 28: {'name': 'The_Climb', 'solved': False}, 29: {'name': 'Modern_Clueless_Child', 'solved': False}, 30: {'name': 'Machine_Fix', 'solved': False}, 31: {'name': 'Prime_Roll', 'solved': False}, 32: {'name': 'Cascade', 'solved': False}, 33: {'name': 'Oreo', 'solved': False}, 34: {'name': 'Escape_Plan', 'solved': False}, 35: {'name': 'Pirates_of_the_Memorial', 'solved': False}, 36: {'name': 'Panda', 'solved': False}, 37: {'name': 'pydis2ctf', 'solved': False}, 38: {'name': 'Mr_Rami', 'solved': False}, 
       39: {'name': 'Commitment', 'solved': False}, 40: {'name': 'AKA', 'solved': False}, 41: {'name': 'Stalin_for_time', 'solved': False}, 42: {'name': 'Where_am_I', 'solved': False}, 43: {'name': 'Vietnam', 'solved': False}, 45: {'name': 'BroBot', 'solved': False}, 46: {'name': 'Flying_Places', 'solved': False}, 47: {'name': 'In_Your_Eyes', 'solved': False}, 48: {'name': 'Secure_Portal', 'solved': False}, 49: {'name': 'Global_Warming', 'solved': False}, 50: {'name': 'Bat_Soup', 'solved': False}, 52: {'name': 'The_Usual_Suspects', 'solved': False}, 53: {'name': 'Body_Count', 'solved': False}, 54: {'name': 'No_DIStractions', 'solved': False}, 55: {'name': 'unseen', 'solved': False}, 56: {'name': 'Smash', 'solved': False}, 57: {'name': 'Friends', 'solved': False}, 58: {'name': 'Lo_Scampo', 'solved': False}, 59: {'name': 'Login_Error', 'solved': False}, 60: {'name': 'little_RSA', 'solved': False}, 61: {'name': 'find32', 'solved': False}, 62: {'name': 'Secret_Society', 'solved': False}, 63: {'name': 'RicknMorty', 'solved': False}, 64: {'name': 'HTB_0x1', 'solved': False}}

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

def run_server():
    if __name__ == '__main__':
        app.run(host=os.getenv('HOST'),port=os.getenv('PORT'))

# t1  = threading.Thread(target=run_server)
# t1.start()

client = commands.Bot(command_prefix='.')

client.remove_command('help')

@client.event
async def on_ready():
    # monitorChallenges.start()
    # challengeStatus.start()
    # checkChallenges.start()
    # firstBlood.start()
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

@tasks.loop(seconds=180)
async def firstBlood():

    allSolved = True
    keys = dict.keys(ch)
    for i in keys:
        if not(ch[i]['solved']):
            allSolved = False

    if(allSolved):
        return
    
    channel = client.get_channel(int(os.getenv('FIRST_BLOOD_CHANNEL')))

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    usernameStr = os.getenv('USER')
    passwordStr = os.getenv('PASSWORD')

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    print('loading')
    browser.get(('https://ctf.csivit.com/login'))
    print('loaded')

    username = browser.find_element_by_id('name-input')
    username.send_keys(usernameStr)
    password = browser.find_element_by_id('password-input')
    password.send_keys(passwordStr)

    submitBtn = browser.find_element_by_class_name('btn-outlined')
    submitBtn.click()


    for i in keys:
        
        if(ch[i]['solved']):
            continue

        browser.get(f'https://ctf.csivit.com/api/v1/challenges/{i}/solves')
        html = browser.page_source
        time.sleep(2)
        html = html[html.index('{'):html.rindex('}')+1]
        y = json.loads(html)
            
        try: y['data']
        except:
            print('key error')
            continue

        if(y['data']==[]):
            continue

        if(y['data']==[]):
            print(f'no data for {ch[i]}')
            continue

        ch[i]['solved'] = True
        # print(f'`First blood for challenge: {ch[i]["name"]} goes to {y["data"][0]["name"]}`')
        print("sending")
        await channel.send(f'```css\n🩸 First blood for .{ch[i]["name"]} goes to [{y["data"][0]["name"]}]```')
    browser.close()


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
    print("send")
    global connectionData
    connectionData={}
    server = socket.gethostbyname('chall.csivit.com')
    channel = client.get_channel(int(os.getenv('CHALLENGE_STATUS_CHANNEL')))
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

    await channel.send(embed=embed)
    print('sent')

@client.command(aliases=['Challenges', 'challenges', 'challenge'])
@commands.has_permissions(kick_members=True)
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


    


client.run(os.getenv('TOKEN'))

#https://discord.com/oauth2/authorize?client_id=723828224307757178&scope=bot
