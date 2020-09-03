import discord
from discord.ext import commands
import gpt_2_simple as gpt2
import os
import config
global convo

convo = config.convo
DISCORD_TOKEN = 'NzQ5NzQ0MTI4ODI0NDQyOTEy.X0wboQ.oNoieSTYTAePGL9x0-K88kmv7Xg'
bot = commands.Bot(command_prefix='$')
bot.remove_command('help')
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')

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
    await ctx.send(config.MESSAGE)

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
    convo_len = len(" ".join(convo)+ f'\n <0> {" ".join(args)} \n <8>')-4
    messages = gpt2.generate(sess,
                      length=70,
                      temperature=0.7,
                      prefix=" ".join(convo)+ f'\n <0> {" ".join(args)} \n <8>',
                      nsamples=5,
                      batch_size=5,
                      return_as_list=True)
    text_polarity = [TextBlob(text).sentiment.polarity for text in a]
    convo.pop(0)
    message_options = []
    convo.append("<0> "+" ".join(args))
    for message_option in messages:
        message = ''
        for i in (a[(convo_len+1):].split('<')[1:]):
          if i[0:1] == '8':
            message+= i[2:]
          else:
            break
        message_options.append(message)
    convo.append("<8> "+sorted(zip(text_polarity,message_options))[0][1])
    await ctx.send("<8> "+sorted(zip(text_polarity,message_options))[0][1])

@bot.command(name='kys', 
            brief='kys',
            pass_context = True)
async def kys(ctx, *args):
    if ctx.author.id in [645940845245104130]:
        await ctx.send(config.MESSAGE)
        import sys
        sys.exit()
    else:
        await ctx.send(f"No! {config.MESSAGE}")

@bot.command(name='reset', 
            brief='reset',
            pass_context = True)
async def reset(ctx, *args):
    if ctx.author.id in [645940845245104130]:
        convo = config.convo
    else:
        await ctx.send("No! Reset yourself!")

@bot.command(name='debug', 
            brief='debug',
            pass_context = True)
async def debug(ctx, *args):
    if ctx.author.id in [645940845245104130]:
        await ctx.send(" ".join(convo))
    else:
        await ctx.send("No!")
bot.run(DISCORD_TOKEN)
