import discord
from discord.ext import commands
import gpt_2_simple as gpt2
import os

global convo
convo = ["<0> We are playing League", "<8> Yes I am Chen","<0> NICE COCK", "<8> FUCK YOU!"]

DISCORD_TOKEN = 'NzQ5NzQ0MTI4ODI0NDQyOTEy.X0wboQ.oNoieSTYTAePGL9x0-K88kmv7Xg'
bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game("League of Legends")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_message(message):
    if message.author == bot.user:
            return
    await bot.process_commands(message)

@bot.command(name='hello', 
            brief='hello',
            pass_context = True)
async def hello(ctx, *args):
    await ctx.send("Fuck you!")

@bot.command(name='help', 
            brief='help',
            pass_context = True)
async def help(ctx, *args):
    await ctx.send("$c to talk to me. After around 3 messages I will be able to speak on topic")

@bot.command(name='c', 
            brief='c',
            pass_context = True)
async def c(ctx, *args):
    print("running AI")
    await ctx.send("Processing.... Please wait 10-20 seconds for a response.", delete_after=5.0)
    global convo
    a = gpt2.generate(sess,
                      length=70,
                      temperature=0.7,
                      prefix=" ".join(convo)+ f'\n <0> {" ".join(args)} \n <8>',
                      nsamples=1,
                      batch_size=1,
                      return_as_list=True)[0]
    convo_len = len(" ".join(convo)+ f'\n <0> {" ".join(args)} \n <8>')-4
    print(a)
    print(a[convo_len:])
    with open("debug.txt","w") as file:
        file.write(a)
    print(convo_len)
    convo.pop(0)
    convo.append("<0> "+" ".join(args))
    message = ''
    for i in (a[(convo_len+1):].split('<')[1:]):
      if i[0:1] == '8':
        message+= i[2:]
      else:
        break
    convo.append("<8> "+message)
    print(convo)
    await ctx.send(message)

@bot.command(name='kys', 
            brief='kys',
            pass_context = True)
async def kys(ctx, *args):
    if ctx.author.id in [645940845245104130]:
        await ctx.send("Fuck you!")
        import sys
        sys.exit()
    else:
        await ctx.send("No! Fuck you!")

@bot.command(name='reset', 
            brief='reset',
            pass_context = True)
async def kys(ctx, *args):
    if ctx.author.id in [645940845245104130]:
        convo = ["<0> We are playing League", "<8> Yes I am Chen","<0> bruh what do you wnat", "<8> to accept the fucking invite","<0> NICE COCK", "<8> FUCK YOU!"]
    else:
        await ctx.send("No! Reset yourself!")
bot.run(DISCORD_TOKEN)
