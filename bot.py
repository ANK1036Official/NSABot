import discord
import urllib.request
from urllib.request import urlopen
import subprocess
import asyncio
import re
import os
import magic
import time
from discord.ext.commands import Bot
from discord.ext import commands
import re
import glob
import pypwned
import json
import sys

TOKEN = ''
HIBP_API = ''
SHODAN_API = ''
HASHESORG_API = ''


#class DevNull:
#    def write(self, msg):
#        pass
#
#sys.stderr = DevNull()

with open("blacklist.json", "r") as blacklist:
    ids = json.load(blacklist)
helpdata = """
Commands:
changelog - View latest changelog.
analyze - Check what a page is running.
checkemail - Check email in data breaches. (Best used with "search" command, chances.)
crack - Attempts to crack a password hash.
honeycheck - Checks if IP belongs to a honeypot. (experimental)
ip2cidr - Get CIDR from IP address.
joke - Tell a dad joke.
namecheck - Find accounts belonging to a username.
search - Get first 20 results from Breach Compilation. (Perms needed)
spyon - Take a screencap of a stolen camera. (Perms needed)
subdomains - Get subdomains from online sources.
target - Send a target for ANK to attack. Accepts an IP, email, or url.
ttcheck - Check onion URL title.

More to come...
"""
changedata = """
░░▒██████▌ ▄████████▄  ░░▒██████ ░░▒████▄  ░░▒██████▄ ███████████
░▒▒███████ ████▄▄  ██  ░▒▒██▌███ ░▒▒█▌███▌ ░▒▒██▌████ ███ ▒██▌███
░▒███▌████ ▐██████▄ ▀  ░▒███▌███ ░▒██▌██▀  ░▒███▌████     ▒▒█▌
▒▒███▌████  ▀▀▀▀ ███▄  ▒▒███████ ▒▒█████▄  ▒▒███▌████     ░▒█▌
▒████▌████ ░▒██ ▄████▌ ▒████▌███ ▒███▌███▌ ▒████▌████     ░▒▒▌
█████▌████ ░████████▀  █████▌███ ███████▀  ▀████████▀     ░░▒▌

Tue 15 Oct 2019 09:33:50 PM EDT

Improved code.
"""

client = commands.Bot(command_prefix='nsa-')
client.remove_command('help')
@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def help(ctx):
    await ctx.send("```"+helpdata+"```")

@client.command()
async def changelog(ctx):
    await ctx.send("```"+changedata+"```")


@client.command()
async def analyze(ctx, arg1):
        if str(ctx.author.id) in(ids):
                await ctx.send("You are banned from using the bot.")
                return
        else:
            authorid = ctx.author.name
            descrim = ctx.author.discriminator
            try:
                print("Log: analysis on "+arg1+" -- "+authorid+"#"+descrim+" ("+str(ctx.author.id)+") | Server: "+str(ctx.author.guild)+" ("+str(ctx.author.guild.id)+")")
            except:
                pass
            if re.match(r'^http', arg1):
                whatwebdata = subprocess.getoutput("whatweb -a 1 --wait=5 --color=never "+arg1+" | head -1")
                if whatwebdata == "":
                    await ctx.send("Unable to retrieve data.")
                else:
                    embed=discord.Embed(color=0x39fd3f)
                    embed.add_field(name="Output:", value=whatwebdata, inline=False)
                    await ctx.send(embed=embed)
            else:
                await ctx.send("```Correct format: http://wahtever.com/```")

@client.command()
async def target(ctx, arg1):
        if str(ctx.author.id) in(ids):
            await ctx.send("You are banned from using the bot.")
            return
        else:
            authorid = ctx.author.name
            descrim = ctx.author.discriminator
            try:
                print("Log: target "+arg1+" -- "+authorid+"#"+descrim+" ("+str(ctx.author.id)+") | Server: "+str(ctx.author.guild)+" ("+str(ctx.author.guild.id)+")")
            except:
                pass
            await ctx.send("Sending target to ANK...")
            f=open("targets.txt", "a+")
            f.write(arg1+" - "+authorid+"#"+descrim+"\n")
            f.close

@client.command()
async def ip2cidr(ctx, arg1):
        if str(ctx.author.id) in(ids):
            await ctx.send("You are banned from using the bot.")
            return
        else:
            authorid = ctx.author.name
            descrim = ctx.author.discriminator
            try:
                print("Log: ip2cidr on "+arg1+" -- "+authorid+"#"+descrim+" ("+str(ctx.author.id)+") | Server: "+str(ctx.author.guild)+" ("+str(ctx.author.guild.id)+")")
            except:
                pass
            cidrdata = subprocess.getoutput("curl -s https://freeapi.robtex.com/ipquery/"+arg1+" | jq '.bgproute'")
            embed=discord.Embed(color=0x39fd3f)
            embed.add_field(name="Output:", value=cidrdata, inline=False)
            await ctx.send(embed=embed)


@client.command()
async def joke(ctx):
    dadjoke = subprocess.getoutput("curl -s -H 'User-Agent: DadBot' -H 'Accept: text/plain' https://icanhazdadjoke.com/")
    await ctx.send(dadjoke)

@client.command()
async def checkemail(ctx, arg1):
        if str(ctx.author.id) in(ids):
            await ctx.send("You are banned from using the bot.")
            return
        else:
            authorid = ctx.author.name
            descrim = ctx.author.discriminator
            try:
                print("Log: checkemail used on "+arg1+" -- "+authorid+"#"+descrim+" ("+str(ctx.author.id)+") | Server: "+str(ctx.author.guild)+" ("+str(ctx.author.guild.id)+")")
            except:
                pass
            await ctx.send("```Checking email, please wait up to 30 seconds...```")
            pwny = pypwned.pwned(HIBP_API)
            s1 = json.dumps(pwny.getAllBreachesForAccount(email=arg1))
            d2 = json.loads(s1)
            finalout = ""
            for finaldata in d2:
                try:
                    finalout += finaldata['Name']+"\n"
                except:
                    finalout == str("Not found or error.")
            if finalout != "":
                await ctx.send("Email found in: \n```"+finalout+"```")
            else:
                await ctx.send("```Not found.```")
            

@client.command()
async def namecheck(ctx, arg1):
        if str(ctx.author.id) in(ids):
            await ctx.send("You are banned from using the bot.")
            return
        else:
            authorid = ctx.author.name
            descrim = ctx.author.discriminator
            
            if ' ' in arg1:
                await ctx.send("```Username cannot have spaces.```")
            else:
                filename = arg1+".txt"
                await ctx.send("This might take a while...")
                subprocess.call(["userrecon-py", "target", arg1, "--positive", "--output"])
                if os.path.isfile(filename):
                    os.remove(filename)
                makefile = open(filename, "w+")
                p = subprocess.Popen("cat "+arg1+".json | jq '.[].url' | sed \'s/\"//g\' > "+filename, stdout=subprocess.PIPE, shell=True)
                p.communicate()
                testsum = 1999
                space = 1
                line = 1
                charc = 1
                with open(filename) as infile:
                    text = infile.read()
                    for i in text:
                        if(i == " "):
                            space += 1
                        elif(i == "\n"):
                            line += 1
                        else:
                            charc += 1
                    if charc > testsum:
                        p = subprocess.Popen("split -l 25 --additional-suffix='.split' "+filename, stdout=subprocess.PIPE, shell=True)
                        p.communicate()
                        for splits in os.listdir():
                            if splits.endswith(".split"):
                                with open(splits, 'r') as filedata:
                                    content_file = filedata.read()
                                    await ctx.send("```"+content_file+"```")
                                    os.remove(splits)
                    else:
                        with open(filename, 'r') as filedata:
                            content_file = filedata.read()
                            await ctx.send("```"+content_file+"```")
                os.remove(arg1.json)
                os.remove(arg1.txt)




@client.command()
async def subdomains(ctx, arg1):
        if str(ctx.author.id) in(ids):
            await ctx.send("You are banned from using the bot.")
            return
        else:
            authorid = ctx.author.name
            descrim = ctx.author.discriminator
            try:
                print("Log: sudomain check on "+arg1+" -- "+authorid+"#"+descrim+" ("+str(ctx.author.id)+") | Server: "+str(ctx.author.guild)+" ("+str(ctx.author.guild.id)+")")
            except:
                pass
            if re.match(r'^([A-Za-z0-9]\.|[A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9]\.){1,3}[A-Za-z]{2,6}$', arg1):
                await ctx.send("Grabbing subdomains from sources...")
                subprocess.call(["/media/root/Leaks/New_Toolkit/Scanners/findomain/findomain-linux", "-t", arg1, "-o"])
                with open('./'+arg1+'.txt', 'r') as content_file:
                    content = content_file.read()
                    await ctx.send("```"+content+"```")
                    os.remove("./"+arg1+".txt")
            else:
                await ctx.send("```Correct format: wahtever.com```")



@client.command()
async def honeycheck(ctx, arg1):
        if str(ctx.author.id) in(ids):
            await ctx.send("You are banned from using the bot.")
            return
        else:
            authorid = ctx.author.name
            descrim = ctx.author.discriminator
            try:
                print("Log: honeypot check on "+arg1+" -- "+authorid+"#"+descrim+" ("+str(ctx.author.id)+") | Server: "+str(ctx.author.guild)+" ("+str(ctx.author.guild.id)+")")
            except:
                pass
            honey = "https://api.shodan.io/labs/honeyscore/" + arg1 + "?key=" + SHODAN_API
            phoney = str(urlopen(honey).read())
            if '0.0' in phoney:
                await ctx.send('Honeypot Probabilty: 0%')
            if '.1' in phoney:
                await ctx.send('Honeypot Probabilty: 10%')
            if '.2' in phoney:
                await ctx.send('Honeypot Probabilty: 20%')
            if '.3' in phoney:
                await ctx.send('Honeypot Probabilty: 30%')
            if '.4' in phoney:
                await ctx.send('Honeypot Probabilty: 40%')
            if '.5' in phoney:
                await ctx.send('Honeypot Probabilty: 50%')
            if '.6' in phoney:
                await ctx.send('Honeypot Probabilty: 60%')
            if '.7' in phoney:
                await ctx.send('Honeypot Probabilty: 70%')
            if '.8' in phoney:
                await ctx.send('Honeypot Probabilty: 80%')
            if '.9' in phoney:
                await ctx.send('Honeypot Probabilty: 90%')
            if '1.0' in phoney:
                await ctx.send('Honeypot Probabilty: 100%')


@client.command()
async def crack(ctx, arg1):
        if str(ctx.author.id) in(ids):
            await ctx.send("You are banned from using the bot.")
            return
        else:
            authorid = ctx.author.name
            descrim = ctx.author.discriminator
            try:
                print("Log: crack on hash "+arg1+" -- "+authorid+"#"+descrim+" ("+str(ctx.author.id)+") | Server: "+str(ctx.author.guild)+" ("+str(ctx.author.guild.id)+")")
            except:
                pass
            hasharg = arg1.lower()
            if "," in hasharg:
                hashdata = subprocess.getoutput("curl -s \"https://hashes.org/api.php?key=" + HASHESORG_API + "&query="+hasharg+"\" | jq --monochrome-output '.result'")
            else:
                hashdata = subprocess.getoutput("curl -s \"https://hashes.org/api.php?key=" + HASHESORG_API + "&query="+hasharg+"\" | jq --monochrome-output '.result | .[\""+hasharg+"\"] | .plain'")
            if hashdata == "":
                await ctx.send("Unable to crack hash.")
            elif "error" in hashdata:
                await ctx.send("Error, only 20 hashes per minute allowed.")
            else:
                await ctx.send("```"+hashdata+"```")

@client.command()
async def spyon(ctx, arg1):
        if str(ctx.author.id) in(ids):
            await ctx.send("You are banned from using the bot.")
            return
        else:
            authorid = ctx.author.name
            descrim = ctx.author.discriminator
            try:
                print("Log: spyon "+arg1+" -- "+authorid+"#"+descrim+" ("+str(ctx.author.id)+") | Server: "+str(ctx.author.guild)+" ("+str(ctx.author.guild.id)+")")
            except:
                pass
            author = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="DadBot Access")
            if role in ctx.author.roles:
                await ctx.send("Screencapping camera...")
                check = subprocess.getoutput("timeout -k 60 ffmpeg -loglevel fatal -rtsp_transport tcp -i 'rtsp://"+arg1+":554/tcp/av0_0' -r 1 -vframes 1 screencap.png")
                await ctx.send(file=discord.File('screencap.png'))
                os.remove("screencap.png")
            else:
                await ctx.send("Role required.")



@client.command()
async def ttcheck(ctx, arg1):
        if str(ctx.author.id) in(ids):
            await ctx.send("You are banned from using the bot.")
            return
        else:
            authorid = ctx.author.name
            descrim = ctx.author.discriminator
            print("Deep title check on "+arg1)
            if re.match(r'^http://|onion/$', arg1):
                await ctx.send("```Checking "+arg1+" for a title...```")
                titledata = subprocess.getoutput("proxychains4 -q -f /etc/proxychains.conf curl -s -U 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0' "+arg1+" | pup 'title text{}'")
                embed=discord.Embed(color=0x39fd3f)
                finaloutput = arg1+" -- "+titledata
                embed.add_field(name="Output:", value=finaloutput, inline=False)
                await ctx.send(embed=embed) 
            else:
                await ctx.send("```Correct format: http://wahtever.onion/```")

@client.command()
async def search(ctx, arg1):
        if str(ctx.author.id) in(ids):
            await ctx.send("You are banned from using the bot.")
            return
        else:
            authorid = ctx.author.name
            descrim = ctx.author.discriminator
            try:
                print("Log: breachsearch on "+arg1+" -- "+authorid+"#"+descrim+" ("+str(ctx.author.id)+") | Server: "+str(ctx.author.guild)+" ("+str(ctx.author.guild.id)+")")
            except:
                pass
            author = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="DadBot Access")
            if role in ctx.author.roles:
                await ctx.send("Searching 20 max results for "+arg1+"...")
                stdoutdata = subprocess.getoutput("/media/root/BigBoiDrive/DBLeaks/BreachCompilation/query.sh "+arg1+" | head -20 | awk '{printf \"%s\\n\", $0}'")
                embed=discord.Embed(color=0x39fd3f)
                embed.add_field(name="Data:", value=stdoutdata, inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Role required.")

client.run(TOKEN)
