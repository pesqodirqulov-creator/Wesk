from pyrogram import Client, filters
from yt_dlp import YoutubeDL
import os

# --- MA'LUMOTLARINGIZNI SHU YERGA YOZING ---
# my.telegram.org saytidan olgan ma'lumotlaringiz:
api_id = 1234567           # O'z api_id raqamingizni yozing
api_hash = "sizning_hash"   # O'z api_hash kodingizni yozing

# Brend sozlamalari:
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
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'quiet': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)['entries'][0]
            title = info.get('title', 'Music')
            
            # Musiqa fayliga brending berish (Metadata)
            # PythonAnywhere-da ffmpeg o'rnatilgan bo'ladi
            os.system(f'ffmpeg -i track.mp3 -metadata artist="{BREND}" -metadata title="{title}" -c copy "final.mp3" -y')

            # Musiqani yuborish
            await message.reply_audio(
                audio="final.mp3",
                caption=f"🎵 **{title}**\n\n📢 Kanal: {KANAL_LINKI}",
                performer=BREND,
                title=title
            )
            
            # Xabarni o'chirish va tozalash
            await status.delete()
            if os.path.exists("track.mp3"): os.remove("track.mp3")
            if os.path.exists("final.mp3"): os.remove("final.mp3")

    except Exception as e:
        await status.edit(f"❌ Xatolik yuz berdi. YouTube bloklangan bo'lishi mumkin.")
        print(f"Xato: {e}")

print("🚀 UserBot ishga tushmoqda...")
app.run()
