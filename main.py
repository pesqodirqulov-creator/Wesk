import os
import asyncio
from pyrogram import Client, filters

# API ma'lumotlaringizni shu yerga yozing
API_ID = 1234567  # O'zingiznikiga almashtiring
API_HASH = "sizning_api_hash_kodingiz" # O'zingiznikiga almashtiring

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start", prefixes=".") & filters.me)
async def start(client, message):
    await message.edit("✅ **Userbot muvaffaqiyatli ishlamoqda!**")

@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping(client, message):
    await message.edit("🚀 **Pong!**")

print("Bot kodi ishga tushdi. Terminalni kuzating...")
app.run()
