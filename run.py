from my_requests.checkCurrency import checkCurrency

# print(checkCurrency())

import discord
import os
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
scheduler = AsyncIOScheduler()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)

    async def run_exchange_alert():
        rate = checkCurrency().conversion_rate
        if rate < 2100:
            await channel.send(f"📈 Exchange rate alert: 1 IDR = {rate:.6f} HKD")
    
    scheduler.add_job(run_exchange_alert, 'interval', hours=6)
    scheduler.start()

bot.run(TOKEN)

