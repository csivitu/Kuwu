import discord
from discord.ext import commands

class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name= 'ban', aliases=['Ban'])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member):
        await member.ban(reason=None)
    

def setup(client):
    client.add_cog(Ban(client))
