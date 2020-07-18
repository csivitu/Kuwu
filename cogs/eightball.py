import discord
from discord.ext import commands
import random

class EightBall(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball', '8Ball'])
    async def _8ball(self, ctx, *, question):
        responses =['It is certain.','It is decidedly so.','Without a doubt.',
                    'Yes – definitely.','You may rely on it.','As I see it, yes.',
                    'Most likely.','Outlook good.','Yes.',
                    'Signs point to yes.',' Reply hazy, try again.','Ask again later.',
                    ' Better not tell you now.',' Cannot predict now.','Concentrate and ask again.',
                    'Don\'t count on it.',' My reply is no.',' My sources say no.',
                    'Outlook not so good.','Very doubtful.']
        
        if '.flag' in question:
            await ctx.channel.purge(limit=1)
            return

        if 'csictf{' in question:
            await ctx.channel.purge(limit=1)
            await ctx.send('Oh no no! Don\'t post flags here.')
        else:
            await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

def setup(client):
    client.add_cog(EightBall(client))