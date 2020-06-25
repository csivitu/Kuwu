import discord
from discord.ext import commands

class About(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name= 'about', aliases=['About', 'AboutCsi', 'AboutCSI', 'aboutCsi', 'aboutCSI'])
    async def about(self, ctx):
        await ctx.send('The Computer Society of India is the largest body of computer professionals in India. We are a group of skilled designers, developers and tech enthusiasts who engage in a lot of projects and hackathons. To help push technology forward, we organise a wide range of workshops, conferences, events and competitions both technical and non-technical.\nWhen we build, it matters.')
    

def setup(client):
    client.add_cog(About(client))