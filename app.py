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

client = Bot(description="Hutli's Server Status",
             command_prefix="!", pm_help=False, )


@client.event
async def on_ready():
    print("Bot is ready!")
    activity = discord.Activity(
        type=discord.ActivityType.watching, name="you all...")
    #activity = discord.CustomActivity(name='Downloading more RAM...')
    await client.change_presence(activity=activity)


@ client.command(pass_context=True)
async def srvstatus(ctx):
    if ctx.message.author.guild_permissions.administrator:
        msg = ''
        info = requests.get(SERVER_URL).json()
        msg += f'Players: {info["OnlinePlayers"]}/{info["TotalPlayers"]}\n\n'
        msg += f'Memory useage: {psutil.virtual_memory().percent}%\n\nCPU Cores:\n'
        for percentage in psutil.cpu_percent(percpu=True, interval=1):
            denominator = 30
            whole_fraction = math.floor(percentage / denominator)
            viz = '█' * whole_fraction
            remaining = denominator - whole_fraction
            modulus = percentage % denominator
            modulus_fraction = denominator / modulus if modulus != 0 else 0
            if modulus_fraction > (2/3):
                viz += '▓'
                remaining -= 1
            elif modulus_fraction > (1/3):
                viz += '▒'
                remaining -= 1
            viz += '░' * remaining
            msg += f"|{viz}| {percentage}%\n"
        msg += (f"Total CPU Usage: {psutil.cpu_percent()}%")
        await ctx.channel.send(msg)
    else:
        await ctx.channel.send("Command only for admins")

client.run(DISCORD_APP_TOKEN)
