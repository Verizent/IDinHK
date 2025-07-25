from my_requests.checkCurrency import checkCurrency

# print(checkCurrency())

import discord
import os
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from keep_run import keep_alive

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
scheduler = AsyncIOScheduler()

# Global Variable
minRate = 10000

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    guild = bot.guilds[0]
    channel = bot.get_channel(CHANNEL_ID)

    role = discord.utils.get(guild.roles, name="IDR Watchers")
    # or use role = guild.get_role(role_id) if you know the role id
    
    if not channel or not role:
        print("❌ Could not find the channel or role. Check CHANNEL_ID or role name.")
        return

    async def reset_min_rate():
        global minRate
        rate = checkCurrency()
        minRate = rate['conversion_rate']
        await channel.send(
            f"📊 **Weekly Exchange Tracker Reset!**\n"
            f"🔁 Starting fresh this week with:\n"
            f"🇮🇩 1 IDR = **{minRate:.2f} HKD 🇭🇰**\n"
            f"Let’s monitor the market and catch the best rates! 💰📉\n\n"
            f"{role.mention}"
        )      
    
    async def run_exchange_alert():
        global minRate
        rate = checkCurrency()
        rate = rate['conversion_rate']

        if rate < minRate:
            minRate = rate
            await channel.send(
                f"📉 **New Weekly Low Alert!**\n"
                f"🚨 The exchange rate just dropped to:\n"
                f"🇮🇩 1 IDR = **{rate:.2f} HKD 🇭🇰**\n"
                f"Lowest so far this week – might be a good time to exchange! 💸\n\n"
                f"{role.mention}"
            )
    
    # Run both tasks once immediately
    # await reset_min_rate()
    # await run_exchange_alert()

    scheduler.add_job(run_exchange_alert, 'interval', hours=1)
    scheduler.add_job(reset_min_rate, 'cron', day_of_week='mon', hour=8)
    scheduler.start()

keep_alive()
bot.run(TOKEN)

