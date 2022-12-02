import discord
import os
from dotenv import load_dotenv
import randfacts as facts
import translators as ts
import googletrans
from googletrans import Translator
import urllib
import re
import random
from datetime import datetime as dt
import requests

load_dotenv()
discordToken = os.getenv('DISCORD_TOKEN')
tenorKey = os.getenv('TENOR_API')
happy_url = "https://raw.githubusercontent.com/russBrown2015/CutePuppyList/main/masterlist_happy"
sassy_url = "https://raw.githubusercontent.com/russBrown2015/CutePuppyList/main/masterlist_sassy"

def get_gif_links(mood):
    if mood == "HAPPY":
        r = requests.get(happy_url)
    elif mood == "SASSY":
        r = requests.get(sassy_url)
        
    if r.status_code == 200:
        list = r.text.splitlines()
        return list[random.randint(0, len(list)-1)]
    else:
        return None

red = 242409527570333698
snapdude = 533746229419704332
russ = 238130863735439361

client = discord.Client()

interpretor = Translator()

langs = googletrans.LANGUAGES
langKey = "ISO-639 Language Keys:"
for key in langs:
    langKey = langKey + "\n" + key + ": " +langs.get(key)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    activity = discord.Activity(name=" with your train of thought", type=0)
    await client.change_presence(activity = activity)
    # channel = client.get_channel(botChannel)
    # await channel.message.send("Your favorite bot is now online")
    # send message to bot channel when the bot is connected
    
@client.event
async def on_message(message):
    user = message.author
    
    if user == client.user:
        return
    
    server = message.guild
    textChannel = message.channel
    currentTime = dt.now()
    
       
    if message.content.upper() == "!FACTS":
        print("Sending Facts to " + str(server)+"."+str(textChannel)+" at " + str(currentTime))
        await message.channel.send("Here's a random fact for you!\n"+facts.get_fact(), reference = message)
        return
    
# TRANSLATION
    if message.content.upper()[0:2] == "!T":
        if message.content.upper() == "!T COMMANDS":
            print("Sending translation commands to " + str(server)+"."+str(textChannel)+" at " + str(currentTime))
            await message.channel.send("To perform a translation enter the following command: \n!T [Phrase/Sentence to be translated] -[from language(optional)] -[to language]\nTo get language Codes enter the command: !T langs", reference = message)
            return
        
        if message.content.upper() == "!T LANGS":
            print("sending language list to " + str(user) + " at " + str(currentTime))
            await user.send(langKey)
            return            
        
        qry = message.content[3:len(message.content)].split("-")
        translateString = qry[0]
        
        if len(qry) == 2:
            toLanguage = re.findall("\w\w\-*\w*\w*",qry[1])[0]
            fromLanguage = interpretor.detect(translateString).lang
        elif len(qry) == 3:
            fromLanguage = re.findall("\w\w\-*\w*\w*",qry[1])[0]
            toLanguage = re.findall("\w\w\-*\w*\w*",qry[2])[0]
        
        try:
            translation = ts.google(translateString, from_language = fromLanguage, to_language = toLanguage)
        except:
            await message.channel.send("This is not a supported language. Type '!T langs' to see all supported languages", reference = message)
            return
            
        
        translateUrl = "https://translate.google.com/?sl="+fromLanguage+"&tl="+toLanguage+"&text="+urllib.parse.quote(translateString)+"&op=translate"
        # embed messages
        try:
            embed = discord.Embed(title= "Translation by Google", url = translateUrl, description = "Click the link to hear your translation")
            embed.add_field(name = "Original Text", value = translateString, inline = True)
            embed.add_field(name = "Translated Text", value = translation, inline = True)
            embed.set_footer(text = "Translated from: " + langs.get(fromLanguage) + " Translated to: " + langs.get(toLanguage))
            
            await message.channel.send(embed = embed, reference = message)
        except:
            await message.channel.send("Here's your Translation: " + translation, reference = message)
        
        return   
    
    if "TAX" in message.content.upper():
        print("sending taxation reminder to " + str(server)+"."+str(textChannel)+" at " + str(currentTime))
        await message.channel.send("Reminder: *Taxation is theft*!", reference = message)
        return
    
    if len(re.findall("BILLIONAIRE[S]?",message.content.upper())) > 0:
        print("sending billionaires reminder to " + str(server)+"."+str(textChannel)+" at " + str(currentTime))
        await message.channel.send("EAT THE RICH!", reference = message)
        return
        
    if len(re.findall("FUCK\w*",message.content.upper()))>0 and len(re.findall("\\\FUCK\w*",message.content.upper())) == 0:
        continueAsking = False
        
        if len(message.content.split(" ")) > 5:
            chance = random.randrange(0,100)
            if chance < 30:
                await message.channel.send("How does that really make you feel " + message.author.mention +"?")
                return
        else:
            continueAsking = True
                    
        if continueAsking == False:
            print("Skipping asking for more information on " + str(server) + "." + str(textChannel) + " with " + str(chance) +"\100 chance.")
            return
        else:  
            if message.content.upper() == "FUCK":
                print("Insulting " + str(user) + " on " + str(server) + "." + str(textChannel) + " at " + str(currentTime))
                await message.channel.send("I wouldn't even fuck " + message.author.mention + " for practice.")
                return
            else:
                print("asking for more information on " + str(server) + "." + str(textChannel) + " at " + str(currentTime))
                about = message.content.split(" ")
                for x in range(0,len(about)):
                    if "FUCK" in about[x].upper():
                        pos = x+1
                        break
                    
                aboutStr = ""
                for x in range(pos,len(about)):
                    aboutStr = aboutStr + " " + about[x]
                
                await message.channel.send("Tell us more about" + aboutStr + " " + message.author.mention)
                return
        
    if message.content.upper() == "GOOD BOT":
        print("Many happy from " + str(server)+"."+str(textChannel)+" at " + str(currentTime))
        output = get_gif_links("HAPPY")
        if output != None:
            await message.channel.send(output)
        else:
            await message.channel.send("The github list is broken, it's probably <@" + str(russ)+">'s fault")
        return
    
    if message.content.upper() == "BAD BOT":
        print("Oh no they didnt! " + str(server)+"."+str(textChannel)+" at " + str(currentTime))
        output = get_gif_links("SASSY")
        if output != None:
            await message.channel.send(output)
        else:
            await message.channel.send("The github list is broken, it's probably <@" + str(red)+">'s fault")
        return
    
    # if message.content.upper() == "TEST":
    #     await message.channel.send("testing mentions <@"+str(red)+">'s")
        

client.run(discordToken)
