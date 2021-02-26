import os
import math
import psutil
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()
DISCORD_APP_TOKEN = os.getenv('DISCORD_APP_TOKEN')

client = Bot(description="Hutli's Server Status",
             command_prefix="!", pm_help=False, )


@client.event
async def on_ready():
    print("Bot is ready!")


@client.command(pass_context=True)
async def srvstatus(ctx):
    if ctx.message.author.guild_permissions.administrator:
        msg = ''
        msg += f'Memory useage: {psutil.virtual_memory().percent}%\n\nCPU Cores:\n'
        for percentage in psutil.cpu_percent(percpu=True, interval=1):
            percentage_denominator = 10
            percentage_fraction = round(
                percentage / percentage_denominator)
            percentage_viz = '█' * percentage_fraction + '░' * \
                (percentage_denominator - percentage_fraction)
            msg += f"|{percentage_viz}| {percentage}%\n"
        msg += (f"Total CPU Usage: {psutil.cpu_percent()}%")
        await ctx.channel.send(msg)
    else:
        await ctx.channel.send("Command only for admins")

client.run(DISCORD_APP_TOKEN)
