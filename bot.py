import discord
import requests
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

load_dotenv()
discordToken = os.getenv('DISCORD_TOKEN')
tenorKey = os.getenv('TENOR_API')

happyLinks = ["https://tenor.com/view/dog-happy-miss-you-tail-gif-24314518",
           "https://tenor.com/view/dog-smile-happy-good-boy-dog-smile-happy-good-boy-gif-21703225",
           "https://tenor.com/view/excited-dog-happy-gif-15784013",
           "https://tenor.com/view/smile-excited-woo-shocked-surprised-gif-15991873",
           "https://tenor.com/view/dogs-welsh-corgi-excited-happy-jumping-gif-18188408",
           "https://tenor.com/view/happy-dog-cutie-animal-lover-gif-23043263",
           "https://tenor.com/view/byuntear-dog-dog-smiling-smile-happy-dog-gif-25742762",
           "https://tenor.com/view/dog-viralhog-pet-tail-wagging-excited-gif-20070867"]

red = 242409527570333698
snapdude = 533746229419704332

client = discord.Client()

interpretor = Translator()

langs = googletrans.LANGUAGES
langKey = "ISO-639 Language Keys:"
for key in langs:
    langKey = langKey + "\n" + key + ": " +langs.get(key)

async def get_happy_links():
    url = "https://raw.githubusercontent.com/russBrown2015/CutePuppyList/main/masterlist"
    r = requests.get(url)
    url_list = r.text.splitlines()
    return(url_list)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
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
        
    if len(re.findall("FUCK\w*",message.content.upper()))>0:
        continueAsking = False
        
        if len(message.content.split(" ")) > 5:
            if random.randrange(0,100) > 30:
                continueAsking = True
        else:
            continueAsking = True
                    
        if continueAsking == False:
            print("Skipping asking for more information")
            return
        else:  
            if message.content.upper() == "FUCK":
                print("Insulting " + user + " on " + str(server) + "." + str(textChannel) + " at " + str(currentTime))
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
        await message.channel.send(happyLinks[random.randint(0, len(get_happy_links()))])
        return

client.run(discordToken)