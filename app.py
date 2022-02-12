import discord
from discord.ext import commands, tasks
from discord.ext.commands.errors import CommandInvokeError
from tkm import tkmgame
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix='₺',
    intents=intents,
    description='Developer: @D1STANG3R'
)


@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
    status.start()


@bot.command()
async def ping(ctx):
    await ctx.send('pong!')


oyun = tkmgame()

@bot.command()
async def tkm(ctx):
    oyun.game(ctx.author)
    if oyun.message:
        await ctx.reply(oyun.getmessage())
    if oyun.gamemessage:
        message = oyun.getgamemessage()
        embed = discord.Embed()
        embed.color = 0xFF0000
        embed.description = f"{message['player1'].mention} **{message['score'][0]}:{message['score'][1]}** {message['player2'].mention}"
        player1history = "-----"
        player2history = "-----"
        if len(message['player1history']) != 0:
            player1history = ""
            for i, val in enumerate(message['player1history']):
                player1history += f"**{i+1}-**{val}\n"

        if len(message['player2history']) != 0:
            player2history = ""
            for i, val in enumerate(message['player2history']):
                player2history += f"**{i+1}-**{val}\n"

        embed.add_field(
            name=f"↓{message['player1'].name}↓",
            value=player1history,
            inline=True
        )
        embed.add_field(
            name=f"↓{message['player2'].name}↓",
            value=player2history,
            inline=True
        )
        embed.set_footer(text=f"Next Player: {message['nextplayer'].name}", icon_url=message['nextplayer'].avatar_url)
        await ctx.reply(embed=embed)


@bot.command()
async def tkmstart(ctx, player1: discord.Member, player2: discord.Member):
    oyun.startgame(player1, player2)
    if oyun.message:
        await ctx.reply(oyun.getmessage())
    if oyun.gamemessage:
        message = oyun.getgamemessage()
        embed = discord.Embed()
        embed.color = 0xFF0000
        embed.title = "Game starting... :rock::roll_of_paper::scissors:"
        embed.description = f"{message['player1'].mention} vs {message['player2'].mention}"
        embed.set_footer(text=f"First Player: {message['currentplayer'].name}", icon_url=message['currentplayer'].avatar_url)
        await ctx.reply(embed=embed)


@bot.command()
async def tkmreset(ctx):
    if oyun.player1 != None and oyun.player2 != None:
        if ctx.author == oyun.player1 or ctx.author == oyun.player2:
            oyun.reset()
            await ctx.reply(oyun.getmessage())
        else:
            await ctx.reply("Only players can reset the game!")
    else:
        await ctx.reply("The game has already been reset")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandInvokeError):
        # max83round
        await ctx.reply("**Table limit reached. To play, please reset the game with the **`₺tkmreset`** command.**")
    else:
        print(error)


@tasks.loop(seconds=1)
async def status():
    if oyun.player1 == None and oyun.player2 == None:
        await bot.change_presence(activity=discord.Game('Taş Kağıt Makas'), status=discord.Status.online)
    else:
        if oyun.score[0] == 0 and oyun.score[1] == 0:
            await bot.change_presence(activity=discord.Game(f'{oyun.player1.name} vs {oyun.player2.name}'), status=discord.Status.dnd)
        else:
            await bot.change_presence(activity=discord.Game(f'{oyun.player1.name} {oyun.score[0]}:{oyun.score[1]} {oyun.player2.name}'), status=discord.Status.dnd)

keep_alive()
print("Bot is running")
token = ""
bot.run(token)
