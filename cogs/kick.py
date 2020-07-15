import discord
from discord.ext import commands

class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name= 'kick', aliases=['Kick'])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member):
        if 'Kuwu' in str(member):
            await ctx.send('You can\'t outsmart me')
            return
        await member.kick(reason=None)
    

def setup(client):
    client.add_cog(Kick(client))

