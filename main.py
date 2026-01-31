import os
import asyncio
import threading
import http.server
import socketserver
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# --- MA'LUMOTLARINGIZ ---
api_id = 32894755
api_hash = "67f6c4bfe4148ee90c1f54376a4da248"
BREND = "WEAK M🦂"
KANAL_LINKI = "https://t.me/weakmwx"

app = Client("my_account", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.me & filters.command("m", prefixes="."))
async def music_dl(client, message):
    query = " ".join(message.command[1:])
    if not query:
        await message.edit("❌ Musiqa nomini yozing!\nNamuna: `.m Konsta`")
        return

    status = await message.edit(f"🔎 **{query}** qidirilmoqda...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'outtmpl': 'track.%(ext)s',
        'quiet': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)['entries'][0]
            title = info.get('title', 'Music')
            file_name = ydl.prepare_filename(info)
            
            await status.edit("📤 **Telegramga yuklanmoqda...**")

            await message.reply_audio(
                audio=file_name,
                caption=f"🎵 **{title}**\n\n📢 Kanal: {KANAL_LINKI}",
                performer=BREND,
                title=title
            )
            
            await status.delete()
            if os.path.exists(file_name): os.remove(file_name)

    except Exception as e:
        await status.edit(f"❌ Xatolik: YouTube yuklashni cheklagan bo'lishi mumkin.")
        print(f"Error: {e}")

# Render o'chib qolmasligi uchun Web Server
def run_web():
    with socketserver.TCPServer(("", 10000), http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_web, daemon=True).start()

print("🚀 Musiqa yuklovchi UserBot ishga tushdi!")
app.run()
