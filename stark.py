import discord
from discord.ext import commands
import datetime
import os
from nltk.chat.util import Chat, reflections
from sklearn.linear_model import SGDClassifier
from pairs import pairs
from dotenv import load_dotenv
from pymongo import MongoClient
import pickle
import random
import re
import asyncio

client = MongoClient("localhost", 27017)
db = client["StarkBotBD"]
collection = "Quest_Rep"

load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix = "!", description = "Bot numéro 1")
date = datetime.datetime.now()

emotion = pickle.load(open("emotion.sav", 'rb'))

class Stark(discord.Client, Chat):

    ## Init : Stark class inherits from discord.Cliend and nltk.Chat
    def __init__(self, pairs, reflections, flag=True):
        discord.Client.__init__(self)
        Chat.__init__(self, pairs, reflections)
        self.flag = flag
        self.flag = True

    ## define bot base commands
    async def use_bot_command(self, mess):
        if mess == "!ping":
            await message.channel.send("Pong !")
        if mess == "!date":
            await message.channel.send("**%s**" % date)
        if mess == "!bonjour":
            await message.channel.send("Bonjour **%s** :smiley:" % message.author)
        if mess == "!shutdown":
            await message.channel.send("Bye bye !")
            await self.logout()



    ## nltk chat bot    
    def nltk_respond(self, message):
        return self.respond(message)

    ## Query Database
    def mongodb_respond(self, mess):
        title = db.Quest_Rep.find({"$text": {"$search": mess}, 'AnswerCount': {"$ne": "0"}},
            {'score': {'$meta': 'textScore'}})
        title.sort([('score', {'$meta': 'textScore'})]).limit(1)
        ParentId = title[0].get("Id")
        all_resp = db.Quest_Rep.find({"ParentId":ParentId}).sort([('Score', -1)]).limit(5)
        list_resp = [resp.get("Body") for resp in all_resp]
        #resp = list_resp[0]
        final_resp = []
        for i in list_resp:
            i = re.sub('<[^<]+?>', '', i)
            final_resp.append(i)

        
        #mongo_resp = re.sub('<[^<]+?>', '', resp)
        return final_resp, ParentId

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await client.get_channel(808617144504811584).send("```   __,_,\n  [_|_/           Hello there i'm Online\n   //\n _//    __            J.A.R.V.I.S\n(_|)   |@@|\n \ \__ \--/ __            Stark Agency\n  \o__|----|  |   __\n      \ }{ /\ )_ / _\ \n      /\__/\ \__O (__\n     (--/\--)    \__/\n     _)(  )(_                                        ID: CAABMBJMOPLR\n    `---''---`\n```")
        
        ## Auto message on start every 5 minutes
        timeout = 60*60  # 5 minutes
        messauto = "```Hey Human !\n\nI would be pleased to help you on any topic in dastascience field !\n\nFeel free to adress me the subject by conversation or question any time.\nFor more information you may just type : !help\n\nActually with my team we are working on an amazing BOT Challenge brief !\nIf you are curious, you may download the brief here :\n\nhttps://cdn.discordapp.com/attachments/783660084395769887/808333411948429322/Brief-IA-Methodes-Agiles_-_Sprint_1.pdf\n\nHave a nice day !```"
        while True:
            await client.get_channel(808617144504811584).send(messauto)
            await asyncio.sleep(timeout)

    
    async def on_message(self, message):
        mess = message.content
        mess = mess.lower() 

        ## Do not respond itself 
        if message.author == self.user:
            return
        else:
            ## Base commands of the bot
            if mess.startswith('!'):
                if mess == "!start":
                    self.flag = True
                    await message.channel.send("Hey there, how can i help you ?")

                if mess == "!stop":
                    self.flag = False
                    await message.channel.send("Thanks for using me !")
                    msg = await message.channel.send("```Evaluate me :```")
                    await msg.add_reaction('😃')
                    await msg.add_reaction('😐')
                    await msg.add_reaction('🙁')
                        
                    reac_list = ['😃','😐','🙁']
                    check = lambda reaction, user: user == message.author and str(reaction) in reac_list

                    try:    
                    # Waiting for the reaction
                        reaction, user = await client.wait_for('reaction_add', check=check, timeout=10.0)
                        bot_ratings = pickle.load(open("bot_rating.sav", 'rb'))
                        if str(reaction) == "😃":
                            bot_ratings.append(2)
                            pickle.dump(bot_ratings, open("bot_rating.sav", 'wb'))
                            await message.channel.send("```Thanks for you'r report```")

                        if str(reaction) == "😐":
                            bot_ratings.append(1)
                            pickle.dump(bot_ratings, open("bot_rating.sav", 'wb'))
                            await message.channel.send("```Thanks for you'r report```")

                        if str(reaction) == "🙁":
                            bot_ratings.append(0)
                            pickle.dump(bot_ratings, open("bot_rating.sav", 'wb'))
                            await message.channel.send("```Thanks for you'r report```") 

                    except asyncio.TimeoutError:
                        await msg.delete()

                if mess == "!shutdown":
                        await message.channel.send("Bye bye !")
                        await self.logout()

                if self.flag == True:
                    if mess.startswith("!emotion"):
                        request = [mess[9:]]
                        feel = emotion.predict(request)
                        await message.channel.send("Emotions : %s" %feel)
                    if mess.startswith("!suggestion"):
                        request = [mess[12:]]
                        await message.channel.send("Thanks **%s** for you'r suggestion : **%s**" %(str(message.author)[:-5], request))
                    if mess.startswith("!imp"):
                        request = [mess[5:]]
                    if mess == "!score":
                        bot_ratings = pickle.load(open("bot_rating.sav", 'rb'))
                        good = bot_ratings.count(2)
                        medium = bot_ratings.count(1)
                        bad = bot_ratings.count(0)
                        await message.channel.send("Ratings of the bot :\n\nGood -> **%s**\nMedium -> **%s**\nBad -> **%s**" % (good, medium, bad))

                    if mess == "!help":
                        await message.channel.send("```css\nHey %s ! I'm .J.A.R.V.I.S. !\n\nI am the super cool robot created by the renowned :STARK-Agency !\nMy masters are teaching me to imitate you to steal your life !\nIn the meantime, I’m gonna explain how I work to make you believe that I am here to help you \n\nAt the moment I am an expert in datasicene. You may adrress me anything on this topic !\n\nYou can use this command bellow :\n\n   - !start -> To start converse with me\n\n   - !stop -> To stop me and evaluate me\n\n   - !suggestion (You'r suggestion) -> To give us suggestion\n\n   - !ping -> Just for fun to respond you Pong.. No in really i give you'r ping latency\n\n   - !date -> To know the actual date and hour before i control this\n\n   - !bonjour -> Just for give you smile\n\n   - !emotion `your message` -> And i will predict how you feel\n\nYou can check my documentation on :http://jarvis.github.com```" % str(message.author)[:-5])
                    if mess == "!ping":
                        await message.channel.send("Pong ! joke.. You'r ping : {:.0f} ms".format(self.latency * 1000))
                    if mess == "!date":
                        await message.channel.send("**%s**" % str(date)[:-7])
                    if mess == "!test":
                        await message.channel.send("```  __,_,\n  [_|_/           Hello there i'm Online\n   //\n _//    __            J.A.R.V.I.S\n(_|)   |@@|\n \ \__ \--/ __            Stark Agency\n  \o__|----|  |   __\n      \ }{ /\ )_ / _\ \n      /\__/\ \__O (__\n     (--/\--)    \__/\n     _)(  )(_                                        ID: CAABMBJMOPLR\n    `---''---`\n```")
                    if mess == "!bonjour":
                        await message.channel.send("Bonjour **%s** :smiley:" % str(message.author)[:-5])
                    if mess == "!shutdown":
                        await message.channel.send("Bye bye !")
                        await self.logout()


                ## Discution
            else:
                if self.flag == True:
                    ## nltk chat part 
                    resp = self.nltk_respond(mess)
                    if resp :
                        await message.channel.send(resp)

                    ## Query mongodb DataBase
                    else:
                        try:
                            resp, quest_id = self.mongodb_respond(mess)
 
                            for i in resp:
                                if len(i) > 1900:
                                    i1 = i[:1900]
                                    i2 = i[1901:]
                                    await message.channel.send(i1)
                                    await message.channel.send(i2)

                                else:
                                    await message.channel.send(i)
                                msg = await message.channel.send("```Would you kindly help us to improve out bot by rating the relevance of the answer```")
                                await msg.add_reaction('👍')
                                await msg.add_reaction('👎')
                            
                                reac_list = ['👍','👎']
                                check = lambda reaction, user: user == message.author and str(reaction) in reac_list
                                try:
                                # Waiting for the reaction
                                    reaction, user = await client.wait_for('reaction_add', check=check, timeout=60.0)

                                    if str(reaction) == "👍":
                                        await message.channel.send("```Thanks for you'r feedback```")
                                        break
                                    if str(reaction) == "👎":
                                        await message.channel.send("```Thanks for you'r feedback\nHelp us to improve with typing : !imp %s ANSWER```"%quest_id)
                                except asyncio.TimeoutError:
                                    await msg.delete()
                                    break  
                        except IndexError:
                            resp = "I'm just a baby of 3 days old, i'm still learning.\nWhat do you mean by **%s** ?"%mess
                            await message.channel.send("%s"%resp)

client = Stark(pairs, reflections)
#client.run(os.getenv("TOKEN"))  
client.run('ODA4NjQ5MTU5OTI1OTU2NjI5.YCJnNw.F2YKC2ubeazi-FUClgK5H7OA9o0')