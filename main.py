# Work with Python 3.6
import discord
import random
from discord.ext import commands
import aiohttp
import pandas as pd

tokenFile = open('token.txt', 'r')
TOKEN = tokenFile.read()

bot = commands.Bot(command_prefix='!')

# @bot.command(name='rollplayer', help='KEKW')
# async def rollplayer(ctx, name):
#     if name == 'Escavadora':
#         embed = discord.Embed(title='Rolls for player Escavadora', color=0xee57e6)
#         embed.add_field(name='Exotic armor roll:', value='Contraverse Hold', inline=False)
#         embed.add_field(name='Kinetic roll:', value='Huckleberry', inline=False)
#         embed.add_field(name='Energy roll:', value='Sole Survivor with perks Fourth Time\'s the Charm and Firing Line', inline=False)
#         embed.add_field(name='Power roll:', value='Love and Death with perks Field Prep and Full Court', inline=False)
#         await ctx.send(embed=embed)
#     else:
#         await ctx.send('I don\'t have data for this name')

@bot.command(name='upload', help='Upload csv file to the bot')
@commands.has_any_role('Dank')
async def upload(ctx, filename):
    if not ctx.message.attachments:
        await ctx.send('You forgot to add the file you idiot.')

    linka = ctx.message.attachments[0].url
    if linka.endswith('.csv'):
        async with aiohttp.ClientSession() as session:
            async with session.get(linka) as resp:
                if resp.status == 200:
                    with open(f'files/{filename}.csv', 'wb+') as file:
                        file.write(await resp.read())
                await ctx.message.attachments[0].save(f'files/{filename}.csv')
                print('message saved')
    else:
        await ctx.send('Wrong file type, make sure it\'s a csv file')

@upload.error
async def upload_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('Please add your name to the command')

#TODO loadnut csv s heavy weaponami, dat na list(?)
#iter cez inventar s weaponami rozdelit do listov s heavy/energy/kinetic
#rollnut random z kazdeho listu
#checknut cez banlist
#cez bungie api dopyt na exotic collection, select random armor for class
#select random exotic wep z collectionu
@bot.command(name='raidroll', help='Rolls weapons and exotics for specified player')
@commands.has_any_role('Dank')
async def raidroll(ctx, playerName, charClass):
    default_heavy_df = pd.read_csv('heavy_weapons.csv', delimiter=',')
    for index, row in default_heavy_df.iterrows():
        print(row['Name'])




@bot.command(name='roll', help='Rolls a value, use map, kinetic or energy after !roll command')
@commands.has_any_role('Warchief', 'Dank', 'Wardancer')
async def roll(ctx, type):
    random.seed()
    if type == 'map':
        result = random.randint(1, 9)
        map_switch = {
            1:'Altar of Flame',
            2:'Bannerfall',
            3:'The Burnout',
            4:'Distant Shore',
            5:'Endless Vale',
            6:'Javelin Fall',
            7:'Meltdown',
            8:'Midtown',
            9:'Wormhaven'
        }
        await ctx.send('The '+type+' roll is '+str(result)+', which is '+map_switch.get(result, 'Esca fucked up'))
    else:
        if type == 'kinetic' or type == 'energy':
            result = random.randint(0, 99)
            wep_switch = {
                0:'Auto Rifle',
                1:'Pulse Rifle',
                2:'Hand Cannon',
                3:'SMG',
                4:'Sidearm',
                5:'The Vow/Wishender',
                6:'Shotgun',
                7:'Slug Shotgun',
                8:'Fusion Rifle',
                9:'Sniper'
            }
            await ctx.send(
                'The ' + type + ' roll is ' + str(result) + ', which is ' + wep_switch.get(int(result / 10), 'Esca fucked up'))
        else:
            await ctx.send('Not a valid command, try typing map, kinetic or energy after the command.')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You fucked something up.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    game = discord.Game('Gambit with blueberries')
    await bot.change_presence(activity=game)


bot.run(TOKEN)