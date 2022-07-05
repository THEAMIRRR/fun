import discord
from discord.ext import commands
import random
import time
import json
import datetime
import os
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
from discord_components import DiscordComponents, Button, ButtonStyle
from math import pi, tau, e, sqrt
import asyncio
from TagScriptEngine import Interpreter, block
from requests import get
import aiohttp

with open("config.json", "r") as file:
    data = json.load(file)
    token = data["token"]
    prefix = data["prefix"]

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())


@bot.event
async def on_ready():
    DiscordComponents(bot)
    activity=discord.Game(name=">bothelp")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("bot is ready!")

 
@bot.command()
async def psn(ctx, member: discord.Member = None):
    member = member or ctx.author
    GaySanj = random.randint(1, 100)
    ProSanj = random.randint(1, 100)
    NoobSanj = 100 - ProSanj
    AdabSanj = random.randint(1, 100)
    embed = discord.Embed(
        title=(f"{member.display_name}" + "\n╔══════════════" + "\n╠ :hotsprings:" + "  Adab Sanj: " + str(AdabSanj) + "%" + "\n╠══════════" + "\n╠ :hotsprings:" + "  Gay Sanj: " + str(GaySanj) + "%" + "\n╠══════════" + "\n╠ :hotsprings:" + "  Pro Sanj: " + str(ProSanj) + "%" + "\n╠══════════" + "\n╠ :hotsprings:" + "  Noob Sanj: " + str(NoobSanj) + "%" + "\n╚══════════════"),
        timestamp = ctx.message.created_at,
        color=discord.Color.random())
    embed.set_footer(text=f"Darkhast az : {ctx.author}", icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embed)
    return
    if member == None:
        embed = discord.Embed(
        title=(f"{ctx.author.name}" + "\n╔══════════════" + "\n╠ :hotsprings:" + "  Adab Sanj: " + str(AdabSanj) + "%" + "\n╠══════════" + "\n╠ :hotsprings:" + "  Gay Sanj: " + str(GaySanj) + "%" + "\n╠══════════" + "\n╠ :hotsprings:" + "  Pro Sanj: " + str(ProSanj) + "%" + "\n╠══════════" + "\n╠ :hotsprings:" + "  Noob Sanj: " + str(NoobSanj) + "%" + "\n╚══════════════"),
        timestamp = ctx.message.created_at,
        color=discord.Color.random())
    embed.set_footer(text=f"Darkhast az : {ctx.author}", icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embed)
    return


@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send(f"پینگ بات :  {round(bot.latency * 1000)}ms")


@bot.command()
async def clear(ctx, amount=5):
    if ctx.author.guild_permissions.manage_messages:
        if amount > 1000 or amount < 1:
            await ctx.send("مقدار وارد شده از لیمیت بات بیشتر میباشد!")
            return
        textchannel: discord.TextChannel = ctx.channel
        await textchannel.purge(limit=amount+1)
        await ctx.send(f"{amount} پیام پاک شد!")
    else:
        await ctx.reply("**شما پرمیشن نیاز برای اجرای کامند را ندارید!**")

@bot.command()
async def moveall(ctx: commands.Context):
    if ctx.author.guild_permissions.move_members:
        if ctx.author.voice != None:
            moved_members = []
            for voice_channel in ctx.guild.voice_channels:
                for member in voice_channel.members:
                    await member.move_to(ctx.author.voice.channel)
                    moved_members.append(member)
            await ctx.reply(f"**  انجام شد!** `{len(moved_members)} نفر` به چنل  `{ctx.author.voice.channel}` اضافه شد")
        else:
            await ctx.reply("**ابتدا وارد یک چنل ویس شوید**")
    else:
        await ctx.reply("**شما پرمیشن نیاز برای اجرای کامند را ندارید!**")


@bot.command()
async def taghvim(ctx: commands.Context):
    now = datetime.datetime.today()
    mm = str(now.month)
    dd = str(now.day)
    yyyy = str(now.year)
    hour = str(now.hour)
    mi = str(now.minute)
    ss = str(now.second)

    embed = discord.Embed(
        title=("تقویم امروز: " + mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss),
        color=discord.Color.random())
    await ctx.reply(embed=embed)


@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx: commands.Context, member: discord.Member, *, reason: str = "None Given"):
    embed = discord.Embed(
        title=f"**user kicked!**", 
        description=f"**kicked users name** : `{member.display_name}`\n**kicked by** : `{ctx.author.display_name}`\n**reason** : `{reason}`", 
        color=0xff0000
        )                                                             
    await ctx.send(embed=embed)
    await member.kick(reason=reason)


@bot.command()
async def ban(ctx: commands.Context, member: discord.Member, *, reason: str = "None Given"):
    if ctx.author.guild_permissions.ban_members: 
        embed = discord.Embed(
           title=f"**user baned!**",
           description=f"**baned users name** : `{member.display_name}`\n**baned by** : `{ctx.author.display_name}`\n**reason** : `{reason}`",
           color=0xff0000
           )
        await ctx.send(embed=embed)
        await member.ban(reason=reason)
    else:
        await ctx.reply("**شما پرمیشن نیاز برای اجرای کامند را ندارید!**")


@bot.command()
async def unban(ctx, *, member):
    if ctx.author.guild_permissions.administrator:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
    else:
        await ctx.reply("**شما پرمیشن نیاز برای اجرای کامند را ندارید!**")


@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.manage_roles:
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        await member.add_roles(mutedRole)
        embed = discord.Embed(title="**user muted!**", description=f"{member.mention} has been muted", color=0xff0000)
        await ctx.send(embed=embed)
    else:
        await ctx.reply("**شما پرمیشن نیاز برای اجرای کامند را ندارید!**")


@bot.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        embed = discord.Embed(title="**user unmuted!**", description=f"{member.mention} has been unmuted", color=0x2dff00)
        await ctx.send(embed=embed)
    else:
        await ctx.reply("**شما پرمیشن نیاز برای اجرای کامند را ندارید!**")


@bot.command()
async def bothelp(ctx: commands.context):
    embed = discord.Embed(
        title=("**God|Fun help commands:**"),
        description=("**Fun :**" + "\n`>calcu , >psn , >wanted , >pp , >flip , >taghvim ,`" + "\n\n**Moderator :**" + "\n`>ping , >moveall , >kick , >ban , >mute , >unmute`" + "\n\n**Game :**" + "\n`>tictactoe(mention 2 users) - >place(number 1-9)`"),
        color=0xffd200
    )
    embed.set_author(icon_url = ctx.author.avatar_url, name = ctx.author.display_name)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/945302216196128818/52d78f9e6f818a26b2bf76bbd41c4c86.png?size=1024")
    await ctx.reply(embed=embed)


@bot.event
async def on_member_join(member : discord.Member):
    channel = await bot.fetch_channel(900251540642754621)

    img = Image.open("img1.png")

    emoji = "https://cdn.discordapp.com/emojis/943562608575905872.gif?size=44&quality=lossless", "https://cdn.discordapp.com/emojis/943562650007273512.gif?size=44&quality=lossless", "https://cdn.discordapp.com/emojis/943562675022102659.gif?size=44&quality=lossless", "https://cdn.discordapp.com/emojis/943562700355678349.gif?size=44&quality=lossless", "https://cdn.discordapp.com/emojis/943562725974499328.gif?size=44&quality=lossless", "https://cdn.discordapp.com/emojis/943562746304282736.gif?size=44&quality=lossless", "https://cdn.discordapp.com/emojis/943562650007273512.gif?size=44&quality=lossless"
    
    font = ImageFont.truetype("OMEGLE.otf", 72)
    font2 = ImageFont.truetype("OMEGLE.otf", 60)
    font3 = ImageFont.truetype("OMEGLE.otf", 48)
    draw = ImageDraw.Draw(img)

    nameserver = "Welcome To God Mine"

    welcome = "WELCOME!"
    name = member.display_name

    draw.text((365, 285), welcome, (255, 255, 255), anchor="ms", font=font)
    draw.text((365, 335), name, fill="white", anchor="ms", font=font2)
    draw.text((365, 383), nameserver, fill="aqua", anchor="ms", font=font3)
    
    img.save("pimg.png")

    await channel.send(file=discord.File("pimg.png"))
    await asyncio.sleep(2)
    os.remove("pimg.png")


@bot.command()
async def testsorat(ctx):
    img = Image.open("back.jpg")
    font = ImageFont.truetype("OMEGLE.otf", 200)
    lower = "abcdefghijklmnopqrstuvwxyz"
    length = 7
    jomle = "".join(random.sample(lower, length))
    draw = ImageDraw.Draw(img)
    draw.text((960, 550), jomle, fill="white", anchor="ms", font=font)

    img.save("test.jpg")
    timer = 10
    await ctx.send("Are you ready?")
    await ctx.send(file=discord.File("test.jpg"))
    time.sleep(0.5)
    starttime = time.time()
    await asyncio.sleep(2)
    os.remove("test.jpg")

    def is_correct(msg):
        return msg.author==ctx.author

    try:
        guess = await bot.wait_for('message', check=is_correct, timeout=timer)
    except asyncio.TimeoutError:
        return await ctx.send("You took too long :(")

    if guess.content == jomle:
        fintime = time.time()
        total = fintime - starttime
        await guess.reply(f"**Good Job!**  {round(total, 2)} seconds")
        
    else:
        await ctx.send("Nope, that wasn't really right")
        fintime = time.time()
        total = starttime - fintime
        await ctx.send(f"{round(total)} seconds")



@bot.command()
async def pp(ctx, member: discord.Member = None):
    member = member or ctx.author

    dick = ("8=D", "8===D", "8=====D", "8=======D",
    "8=========D", "8===========D", "8=============D",
    "8===============D", "8=================D", "8===================D", "8=====================D",
    "8=======================D", "8=========================D", "8===========================D")
    sizeDick = random.choice(dick)

    if sizeDick == "8=D":
        size = "2cm"
    if sizeDick == "8===D":
        size = "4cm"
    if sizeDick == "8=====D":
        size = "6cm"
    if sizeDick == "8=======D":
        size = "8cm"
    if sizeDick == "8=========D":
        size = "10cm"
    if sizeDick == "8===========D":
        size = "12cm"
    if sizeDick == "8=============D":
        size = "14cm"
    if sizeDick == "8===============D":
        size = "16cm"
    if sizeDick == "8=================D":
        size = "18cm"
    if sizeDick == "8===================D":
        size = "20cm"
    if sizeDick == "8=====================D":
        size = "22cm"
    if sizeDick == "8=======================D":
        size = "24cm"
    if sizeDick == "8=========================D":
        size = "26cm"
    if sizeDick == "8===========================D":
        size = "28cm"
    
    embed = discord.Embed(
        title=(sizeDick),
        description=("\nyour dick size is : " + (size)),
        color=discord.Color.random()
    )
    embed.set_author(icon_url = member.avatar_url, name = member.display_name)
    await ctx.send(embed=embed)
    return
    if member == None:
        embed = discord.Embed(
        title=(sizeDick),
        description=("\nyour dick size is : " + (size)),
        color=discord.Color.random()
    )
    embed.set_author(icon_url = ctx.author.avatar_url, name = ctx.author.name)
    await ctx.send(embed=embed)
    return

        



@bot.command()
async def wanted(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    wanted = Image.open("wanted.jpg")
    asset = member.avatar_url_as(size = 128)

    data = BytesIO(await asset.read())

    pfp = Image.open(data)
    pfp = pfp.resize((187,187))

    wanted.paste(pfp, (117,212))
    wanted.save("profile.jpg")

    await ctx.reply(file = discord.File("profile.jpg"))
    await asyncio.sleep(2)
    os.remove("profile.jpg")


player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@bot.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver
    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            myEmbed = discord.Embed(title= "GAME IN PROGRESS",description="IT IS <@" + str(player1.id) + ">'s TURN.",color=0xe74c3c)
            await ctx.send(embed=myEmbed)
        elif num == 2:
            turn = player2
            myEmbed = discord.Embed(title= "GAME IN PROGRESS",description="IT IS <@" + str(player2.id) + ">'s TURN.",color=0xe74c3c)
            await ctx.send(embed=myEmbed)
    else:
        myEmbed = discord.Embed(title= "GAME IN PROGRESS",description="A GAME IS STILL IN PROGRESS. FINISH IT BEFORE STARTING A NEW ONE",color=0xe74c3c)
        await ctx.send(embed=myEmbed)

@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver
    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    myEmbed = discord.Embed(title= "WINNER!",description=mark + " :crown: ",color=0xf1c40f)
                    await ctx.send(embed=myEmbed)
                elif count >= 9:
                    gameOver = True
                    myEmbed = discord.Embed(title= "TIE",description="IT'S A TIE :handshake:",color=0xf1c40f)
                    await ctx.send(embed=myEmbed)

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                myEmbed = discord.Embed(title= "PLACE ERROR!",description="BE SURE TO CHOOSE AN INTEGER BETWEEN 1 AND 9 (INCLUSIVE) AND AN UNMARKED TILE. ",color=0xe74c3c)
                await ctx.send(embed=myEmbed)
        else:
            myEmbed = discord.Embed(title= "TURN ERROR!",description="IT'S NOT YOUR TURN",color=0xe74c3c)
            await ctx.send(embed=myEmbed)
    else:
        myEmbed = discord.Embed(title= "START GAME",description="TO START A NEW GAME, USE -tictactoe COMMAND",color=0x2ecc71)
        await ctx.send(embed=myEmbed)

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        myEmbed = discord.Embed(title= "MENTION ERROR!",description="PLEASE MENTION 2 USERS",color=0xe74c3c)
        await ctx.send(embed=myEmbed)
    elif isinstance(error, commands.BadArgument):
        myEmbed = discord.Embed(title= "ERROR!",description="PLEASE MAKE SURE TO MENTION/PING PLAYERS (ie. <@688534433879556134>)",color=0xe74c3c)
        await ctx.send(embed=myEmbed)

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        myEmbed = discord.Embed(title= "NO POSITION",description="PLEASE ENTER A POSITION TO MARK",color=0xe74c3c)
        await ctx.send(embed=myEmbed)
    elif isinstance(error, commands.BadArgument):
        myEmbed = discord.Embed(title= "INTEGER ERROR!",description="PLEASE MAKE SURE IT'S AN INTEGER",color=0xe74c3c)
        await ctx.send(embed=myEmbed)


@bot.command()
async def flip(ctx,):
    coin = ["shir", "khat"]
    flipchoice = random.choice(coin)
    embed = discord.Embed(
        title=("You flipped : " + (flipchoice)), 
        color=discord.Color.random()
        )
    embed.set_author(icon_url = ctx.author.avatar_url, name = ctx.author.display_name)
    await ctx.send(embed=embed)


blocks = [
    block.MathBlock(),
    block.RandomBlock(),
    block.RangeBlock(),
]
engine = Interpreter(blocks)

data = {
    "1":"¹",
    "2":"²",
    "3":"³",
    "4":"⁴",
    "5":"⁵",
    "6":"⁶",
    "7":"⁷",
    "8":"⁸",
    "9":"⁹"
}

normal_components = [
    [
        Button(style=ButtonStyle.grey, label="1", id="1"),
        Button(style=ButtonStyle.grey, label="2", id="2"),
        Button(style=ButtonStyle.grey, label="3", id="3"),
        Button(style=ButtonStyle.blue, label="×", id="*"),
        Button(style=ButtonStyle.red, label="Exit", id="Exit"),
    ],
    [
        Button(style=ButtonStyle.grey, label="4", id="4"),
        Button(style=ButtonStyle.grey, label="5", id="5"),
        Button(style=ButtonStyle.grey, label="6", id="6"),
        Button(style=ButtonStyle.blue, label="÷", id="/"),
        Button(style=ButtonStyle.red, label="⌫", id="⌫"),
    ],
    [
        Button(style=ButtonStyle.grey, label="7", id="7"),
        Button(style=ButtonStyle.grey, label="8", id="8"),
        Button(style=ButtonStyle.grey, label="9", id="9"),
        Button(style=ButtonStyle.blue, label="+", id="+"),
        Button(style=ButtonStyle.red, label="Clear", id="Clear"),
    ],
    [
        Button(style=ButtonStyle.grey, label="00", id="00"),
        Button(style=ButtonStyle.grey, label="0", id="0"),
        Button(style=ButtonStyle.grey, label=".", id="."),
        Button(style=ButtonStyle.blue, label="-", id="-"),
        Button(style=ButtonStyle.green, label="=", id="="),
    ],
    [
        Button(style=ButtonStyle.green, label="❮", id="❮"),
        Button(style=ButtonStyle.green, label="❯", id="❯"),
        Button(
            style=ButtonStyle.grey,
            label="Change to scientific mode",
            emoji="\U0001f9d1\u200D\U0001f52c",
            id="scientific_mode",
        ),
    ],
]

scientific_components = [
    [
        Button(style=ButtonStyle.grey, label="(", id="("),
        Button(style=ButtonStyle.grey, label=")", id=")"),
        Button(style=ButtonStyle.grey, label="000", id="000"),
        Button(style=ButtonStyle.blue, label="×", id="*"),
        Button(style=ButtonStyle.red, label="Exit", id="Exit"),
    ],
    [
        Button(style=ButtonStyle.grey, label="X²"),
        Button(style=ButtonStyle.grey, label="X³"),
        Button(style=ButtonStyle.grey, label="Xˣ"),
        Button(style=ButtonStyle.blue, label="÷", id="/"),
        Button(style=ButtonStyle.red, label="⌫", id="⌫"),
    ],
    [
        Button(style=ButtonStyle.grey, label="e", id="e"),
        Button(style=ButtonStyle.grey, label="τ", id="τ"),
        Button(style=ButtonStyle.grey, label="π", id="π"),
        Button(style=ButtonStyle.blue, label="+", id="+"),
        Button(style=ButtonStyle.red, label="Clear", id="Clear"),
    ],
    [
        Button(style=ButtonStyle.grey, label=" ", disabled=True),
        Button(style=ButtonStyle.grey, label=" ", disabled=True),
        Button(style=ButtonStyle.grey, label=" ", disabled=True),
        Button(style=ButtonStyle.blue, label="-", id="-"),
        Button(style=ButtonStyle.green, label="=", id="="),
    ],
    [
        Button(style=ButtonStyle.green, label="❮", id="❮"),
        Button(style=ButtonStyle.green, label="❯", id="❯"),
        Button(
            style=ButtonStyle.grey,
            label="Change to normal modeㅤ",
            emoji="\U0001f468\u200D\U0001f3eb",
            id="normal_mode",
        ),
    ],
]

def calculate(expression:str):
    result=''
    expression = expression.replace("π", str(pi))
    expression = expression.replace("τ", str(tau))
    expression = expression.replace("e", str(e))
    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")

    for i in data:
        if data[i] in expression:
            expression = expression.replace(data[i], f"^{i}")

    result = engine.process("{m:"+expression+"}").body
    result = result.replace("{m:", "").replace("}", "")

    try:
        result = f"{float(result):,}"
    except:
        if result == expression:
            result = "∞"
        else:
            result = "Syntax Error!\nDon't forget the sign(s) ('×', '÷', ...).\nnot: 3(9+1) but 3×(9+1)"

    return result

def input_formatter(original:str, label:str):
    if 'Syntax Error!' in original:
        original='|'
    lst=list(original)
    try:
        index=lst.index('|')
        lst.remove('|')
    except:
        index=0
    if label == 'X²':
        lst.insert(index, '²')
    elif label == 'X³':
        lst.insert(index, '³')
    elif label == 'Xˣ':
        lst.insert(index, '^')
    else:
        if len(lst)>1 and lst[index-1]=="^":
            try:
                lst.insert(index, data[label])
                lst.remove('^')
                index-=1
            except:
                lst.insert(index, label)
        else:
            lst.insert(index, label)
    lst.insert(index+1, '|')
    original=''.join(lst)
    return original

def _get_embed(ctx, embed_description:str):
    embed = discord.Embed(
        title=f"{ctx.author}'s calculator",
        description=embed_description,
        color=0x2F3136,
    )
    embed.set_thumbnail(url=ctx.author.avatar_url)
    return embed


@bot.command(aliases=['calc', 'calculator'])
@commands.max_concurrency(1, per=commands.BucketType.user)
async def calcu(ctx):
    affichage = "|"
    is_normal_mode = True
    embed = _get_embed(ctx, f"```{affichage}```")
    expression = ""
    message = await ctx.send(
        components=normal_components, embed=embed,
    )

    while True:
        try:
            interaction = await bot.wait_for(
                "button_click",
                check=lambda inter: inter.author.id == ctx.author.id and inter.message.id == message.id,
                timeout=60,
            )
        except asyncio.TimeoutError:
            return await message.edit(
                embed=_get_embed(ctx, f"```{affichage}```"),
                components=[
                    row.disable_components()
                    for row in interaction.message.components
                ],
            )

        if interaction.custom_id == "Exit":
            embed = _get_embed(ctx, interaction.message.embeds[0].description)
            return await interaction.edit_origin(
                embed=embed,
                components=[
                    row.disable_components()
                    for row in interaction.message.components
                ],
            )
        elif interaction.custom_id == "⌫":
            lst = list(interaction.message.embeds[0].description.replace("`", ""))
            if len(lst) > 1:
                try:
                    index = lst.index("|")
                    x = index - 2
                    y = index + 1
                    if lst[x] == "×" and lst[y] == "×":
                        lst.pop(index - 1)
                        lst.pop(index - 2)
                    else:
                        lst.pop(index - 1)
                except:
                    lst = ["|"]
            affichage = "".join(lst)
            expression = affichage
        elif interaction.custom_id == "Clear":
            expression = ""
            affichage = "|"
        elif interaction.custom_id == "=":
            if "Syntax Error!" in affichage or affichage == "|":
                affichage = "|"
            else:
                expression = expression.replace("|", "")
                expression = calculate(expression)
                affichage = f"{affichage.replace('|','')}={expression}"
            expression = ""
        elif interaction.custom_id == "❮":
            lst = list(interaction.message.embeds[0].description.replace("`", ""))
            if len(lst) > 1:
                try:
                    index = lst.index("|")
                    lst.remove("|")
                    lst.insert(index - 1, "|")
                except:
                    lst = ["|"]
            affichage = "".join(lst)
        elif interaction.custom_id == "❯":
            lst = list(interaction.message.embeds[0].description.replace("`", ""))
            if len(lst) > 1:
                try:
                    index = lst.index("|")
                    lst.remove("|")
                    lst.insert(index + 1, "|")
                except:
                    lst = ["|"]
            affichage = "".join(lst)
        elif interaction.custom_id == "scientific_mode":
            is_normal_mode = False
            await interaction.edit_origin(
                embed=_get_embed(ctx, f"```{affichage}```"),
                components=scientific_components,
            )
        elif interaction.custom_id == "normal_mode":
            is_normal_mode = True
            await interaction.edit_origin(
                embed=_get_embed(ctx, f"```{affichage}```"),
                components=normal_components,
            )
        else:
            if "=" in affichage:
                affichage = ""
            expression = input_formatter(
                original=affichage, label=interaction.component.label
            )
            affichage = expression

        if interaction.custom_id not in ["scientific_mode", "normal_mode"]:
            if is_normal_mode:
                await interaction.edit_origin(
                    embed=_get_embed(ctx, f"```{affichage}```"),
                    components=normal_components,
                )
            else:
                await interaction.edit_origin(
                    embed=_get_embed(ctx, f"```{affichage}```"),
                    components=scientific_components,
                )

@bot.command()
async def server(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name} Info", description="Information of this Server", color=discord.Colour.blue())
    embed.add_field(name='🆔Server ID', value=f"{ctx.guild.id}", inline=True)
    embed.add_field(name='📆Created On', value=ctx.guild.created_at.strftime("%b %d %Y"), inline=True)
    embed.add_field(name='👑Owner', value=f"{ctx.guild.owner.mention}", inline=True)
    embed.add_field(name='👥Members', value=f'{ctx.guild.member_count} Members', inline=True)
    embed.add_field(name='💬Channels', value=f'{len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice', inline=True)
    embed.add_field(name='🌎Region', value=f'{ctx.guild.region}', inline=True)
    embed.set_thumbnail(url=ctx.guild.icon_url) 
    embed.set_footer(text="⭐ • Duo")    
    embed.set_author(name=f'{ctx.author.name}', icon_url=ctx.message.author.avatar_url)

    await ctx.send(embed=embed)


@bot.command()
async def userinfo(ctx, *, member: discord.Member = None): # b'\xfc'
    if member is None:
        member = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=member.mention)
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Joined", value=member.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(member)+1))
    embed.add_field(name="Registered", value=member.created_at.strftime(date_format))
    if len(member.roles) > 1:
        role_string = ' '.join([r.mention for r in member.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(member.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(member.id))
    return await ctx.send(embed=embed)


bot.run(token)