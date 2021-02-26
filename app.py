import os
import math
import psutil
import discord
import requests
from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()
DISCORD_APP_TOKEN = os.getenv('DISCORD_APP_TOKEN')
SERVER_URL = os.getenv('SERVER_URL')

DENOMINATOR = 30

client = Bot(description="Hutli's Server Status",
             command_prefix="!", pm_help=False, )


def get_viz(percentage):
    procent_point = 100 / DENOMINATOR
    whole_fraction = math.floor(percentage / procent_point)
    viz = '█' * whole_fraction
    remaining = DENOMINATOR - whole_fraction
    modulus_fraction = percentage % procent_point
    if modulus_fraction > (2/3):
        viz += '▓'
        remaining -= 1
    elif modulus_fraction > (1/3):
        viz += '▒'
        remaining -= 1
    viz += '░' * remaining
    return f'|{viz}|'


@client.event
async def on_ready():
    print("Bot is ready!")
    activity = discord.Activity(
        type=discord.ActivityType.watching, name="you all...")
    # activity = discord.CustomActivity(name='Downloading more RAM...')
    await client.change_presence(activity=activity)


@ client.command(pass_context=True)
async def srvstatus(ctx):
    if ctx.message.author.guild_permissions.administrator:
        msg = ''
        info = requests.get(SERVER_URL).json()
        msg += f'Players: {info["OnlinePlayers"]}/{info["TotalPlayers"]}\n\n'
        msg += f'Memory useage:\n'
        mem_percent = psutil.virtual_memory().percent
        msg += f'{get_viz(mem_percent)} {mem_percent}%\n\n'
        msg += 'CPU Cores:\n'

        for percentage in psutil.cpu_percent(percpu=True, interval=1):
            msg += f"{get_viz(percentage)} {percentage}%\n"
        msg += (f"Total CPU Usage: {psutil.cpu_percent()}%")
        await ctx.channel.send(msg)
    else:
        await ctx.channel.send("Command only for admins")

client.run(DISCORD_APP_TOKEN)
