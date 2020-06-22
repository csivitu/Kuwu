import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    await client.change_presence(status =  discord.Status.online, activity=discord.Game('Type .list to list all commands'))
    print('Bot is ready')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

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

client.run(os.environ['TOKEN'])

#https://discord.com/oauth2/authorize?client_id=723828224307757178&scope=bot