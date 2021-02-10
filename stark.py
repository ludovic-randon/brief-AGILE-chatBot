import discord
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix = "!", description = "Bot numéro 1")
date = datetime.datetime.now()

class Stark(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author == self.user:
            return
        mess = message.content
        mess = mess.lower() 
        if mess == "!ping":
            await message.channel.send("Pong !")
        if mess == "!date":
            await message.channel.send("**%s**" % date)
        if mess == "!bonjour":
            await message.channel.send("Bonjour **%s** :smiley:" % message.author)
        if mess == "!shutdown":
            await message.channel.send("Bye bye !")
            await bot.logout()

client = Stark()
client.run('ODA4NjQ5MTU5OTI1OTU2NjI5.YCJnNw.F2YKC2ubeazi-FUClgK5H7OA9o0')