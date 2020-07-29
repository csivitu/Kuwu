import discord
from discord.ext import commands, tasks
import os, socket
from dotenv import load_dotenv
import threading, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
load_dotenv()




global challenges
challenges = {'pwn-intended-0x1':30001, 'pwn-intended-0x2':30007, 'pwn-intended-0x3':30013, 'Global Warming':30023, 'Cascade':30203, 'find32':30630,
              'CCC':30215, 'File Library':30222, 'Mr Rami':30231, 'Oreo':30243, 'The Confused Deputy':30256,'The Usual Suspects':30279, 'Warm Up':30272, 'Secure Portal':30281,
              'Escape Plan':30419, 'Prison Break':30407, 'Blaise':30808, 'Vietnam':30814, 'AKA':30611, 'Where am I':30623, 'Login Error':30431, 'Body Count':30202,
              'Friends':30425, 'RicknMorty':30827, 'Secret Society': 30041, 'Smash':30046}

global ch
# ch =  {13: {'name': 'Esrever', 'solved': False}, 14: {'name': 'Rivest_Shamir_Adleman', 'solved': False}, 15: {'name': 'Archenemy', 'solved': False}, 16: {'name': 'pwn_intended_0x2', 'solved': False}, 17: {'name': 'Blaise', 'solved': False}, 18: {'name': 'pwn_intended_0x1', 'solved': False}, 19: {'name': 'pwn_intended_0x3', 'solved': False}, 20: {'name': 'Prison_Break', 'solved': False}, 21: {'name': 'CCC', 'solved': False}, 22: {'name': 'File_Library', 'solved': False}, 24: {'name': 'The_Confused_Deputy', 'solved': False}, 25: {'name': 'Warm_Up', 'solved': False}, 26: {'name': 'Gradient_sky', 'solved': False}, 27: {'name': 'Mein_Kampf', 'solved': False}, 28: {'name': 'The_Climb', 'solved': False}, 29: {'name': 'Modern_Clueless_Child', 'solved': False}, 30: {'name': 'Machine_Fix', 'solved': False}, 31: {'name': 'Prime_Roll', 'solved': False}, 32: {'name': 'Cascade', 'solved': False}, 33: {'name': 'Oreo', 'solved': False}, 34: {'name': 'Escape_Plan', 'solved': False}, 35: {'name': 'Pirates_of_the_Memorial', 'solved': False}, 36: {'name': 'Panda', 'solved': False}, 37: {'name': 'pydis2ctf', 'solved': False}, 38: {'name': 'Mr_Rami', 'solved': False}, 
#        39: {'name': 'Commitment', 'solved': False}, 40: {'name': 'AKA', 'solved': False}, 41: {'name': 'Stalin_for_time', 'solved': False}, 42: {'name': 'Where_am_I', 'solved': False}, 43: {'name': 'Vietnam', 'solved': False}, 45: {'name': 'BroBot', 'solved': False}, 46: {'name': 'Flying_Places', 'solved': False}, 47: {'name': 'In_Your_Eyes', 'solved': False}, 48: {'name': 'Secure_Portal', 'solved': False}, 49: {'name': 'Global_Warming', 'solved': False}, 50: {'name': 'Bat_Soup', 'solved': False}, 52: {'name': 'The_Usual_Suspects', 'solved': False}, 53: {'name': 'Body_Count', 'solved': False}, 54: {'name': 'No_DIStractions', 'solved': False}, 55: {'name': 'unseen', 'solved': False}, 56: {'name': 'Smash', 'solved': False}, 57: {'name': 'Friends', 'solved': False}, 58: {'name': 'Lo_Scampo', 'solved': False}, 59: {'name': 'Login_Error', 'solved': False}, 60: {'name': 'little_RSA', 'solved': False}, 61: {'name': 'find32', 'solved': False}, 62: {'name': 'Secret_Society', 'solved': False}, 63: {'name': 'RicknMorty', 'solved': False}, 64: {'name': 'HTB_0x1', 'solved': False}}

ch =  {69: {'name': 'HTB_0x3', 'solved': False}, 70: {'name': 'HTB_0x6', 'solved': False}, 73: {'name': 'HTB_0x4', 'solved': False}}



global connectionData
connectionData = {}


client = commands.Bot(command_prefix='.')

client.remove_command('help')

@client.event
async def on_ready():
    checkChallenges.start()
    firstBlood.start()
    await client.change_presence(status =  discord.Status.online, activity=discord.Game('Type .list to list all commands'))
    print('Bot is ready')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')






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

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options )

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
    print('Completed!')


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
