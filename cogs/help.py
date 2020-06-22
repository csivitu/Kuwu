import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'help', aliases = ['Help'])
    async def help(self, ctx):
        await ctx.send("List of Command:\n1. Ban: Can be used to ban a member ->\n\t Format: '.ban @username'. Can only be used by member with ban privileges.\n1. Kick: Can be used to kick a member  ->\n\t Format: '.kick @username'. Can only be used by member with kick privileges.\n3. Ping: Can tell you the ping of the bot ->\n\t Format: '.ping'\n4. 8ball: Will help you take decisions, have fun with this one ->\n\t Format: '.8ball question?' ")

def setup(client):
    client.add_cog(Help(client))
    