import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='../')

class autoresponse(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        channel = self.client.get_channel(message.channel.id)
        message.content = message.content.lower().replace(' ','')

        if not('DMChannel' in str(type(message.channel))):
            if '.flag' in message.content:
                await channel.purge(limit=1)
                await channel.send('Ssssshhhh, not here. DM me maybe ;)')
        else:
            return
            

        if 'csictf{' in message.content:
            await channel.purge(limit=1)
            await channel.send(f'<@!{message.author.id}> don\'t post flags here!')


def setup(client):
    client.add_cog(autoresponse(client))
