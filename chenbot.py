import discord
from discord.ext import commands
import gpt_2_simple as gpt2
import os
import config
from textblob import TextBlob

global convo

convo = config.convo
DISCORD_TOKEN = config.discord_token
admins = config.admin_ids

bot = commands.Bot(command_prefix="$")
bot.remove_command("help")

if not os.path.isdir(os.path.join("models", "355M")):
    gpt2.download_gpt2(model_name="355M")

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name="run1")


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    game = discord.Game("League of Legends")
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


@bot.command(name="hello", brief="hello", pass_context=True)
async def hello(ctx, *args):
    await ctx.send(config.MESSAGE)


@bot.command(name="help", brief="help", pass_context=True)
async def help(ctx, *args):
    await ctx.send(
        "$c to talk to me. After around 3 messages I will be able to speak on topic"
    )


@bot.command(name="c", brief="c", pass_context=True)
async def c(ctx, *args):
    """ Takes user's message and runs the trained GPT2 model on the message to predict 5 probable continuations
       
    Out of the 5 continutations, textblob selects the most negative in sentiment
    """
    if len(args) == 0:
        await ctx.send("You didn't say anything retard!")
        return
    print("running AI")
    await ctx.send(
        "Processing.... Please wait 10-20 seconds for a response.", delete_after=5.0
    )
    global convo
    convo_len = len(" ".join(convo) + f'\n <0> {" ".join(args)} \n <8>') - 4
    messages = gpt2.generate(
        sess,
        length=70,
        temperature=0.7,
        prefix=" ".join(convo) + f'\n <0> {" ".join(args)} \n <8>',
        nsamples=5,
        batch_size=5,
        return_as_list=True,
    )
    text_polarity = [TextBlob(text).sentiment.polarity for text in messages]
    convo.pop(0)
    message_options = []
    convo.append("<0> " + " ".join(args))
    for message_option in messages:
        message = ""
        for i in message_option[(convo_len + 1) :].split("<")[1:]:
            if i[0:1] == "8":
                message += i[2:]
            else:
                break
        message_options.append(message)
    convo.append("<8> " + sorted(zip(text_polarity, message_options))[0][1])
    await ctx.send(sorted(zip(text_polarity, message_options))[0][1])


@bot.command(name="kys", brief="kys", pass_context=True)
async def kys(ctx, *args):
    """ Kills the bot if an admin send the kys command
       
    Mainly used for debug
    """
    if ctx.author.id in admins:
        await ctx.send(config.MESSAGE)
        import sys

        sys.exit()
    else:
        await ctx.send(f"No! {config.MESSAGE}")


@bot.command(name="reset", brief="reset", pass_context=True)
async def reset(ctx, *args):
    """ Resets the conversation to the original conversation defined in config.py if the user is an admin (defined in config.py)
       
    Mainly used for debug
    """
    if ctx.author.id in admins:
        convo = config.convo
    else:
        await ctx.send("No! Reset yourself!")


@bot.command(name="debug", brief="debug", pass_context=True)
async def debug(ctx, *args):
    """ Sends the current conversation status to the discord chat (if sent by an admin)
       
    Mainly used for debug
    """
    if ctx.author.id in admins:
        await ctx.send(" ".join(convo))
    else:
        await ctx.send("No!")


bot.run(DISCORD_TOKEN)
