import os
import random
import requests
import discord
from discord.ext import commands

# --- Ayarlar ---
TOKEN = os.getenv("DISCORD_TOKEN")  # .env veya sistem değişkeni kullanman daha güvenli
DOSYA_ADI = "kasa_sayisi.txt"

# --- Intents ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

emojiler = ["\U0001F600", "\U0001F606", "\U0001F923"]
event1 = False

# --- Yardımcı: Kasa sayısı dosyası ---
def _dosya_ilklendir():
    if not os.path.exists(DOSYA_ADI):
        with open(DOSYA_ADI, "w", encoding="utf-8") as f:
            f.write("0")

def _kasa_sayisini_oku() -> int:
    _dosya_ilklendir()
    with open(DOSYA_ADI, "r", encoding="utf-8") as f:
        icerik = f.read().strip() or "0"
        try:
            return int(icerik)
        except ValueError:
            return 0

def _kasa_sayisini_yaz(yeni_deger: int):
    with open(DOSYA_ADI, "w", encoding="utf-8") as f:
        f.write(str(yeni_deger))

# --- Olaylar / Komutlar ---
@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yaptık.")

@bot.command()
async def merhaba(ctx):
    await ctx.send("Selam!")

@bot.command()
async def bye(ctx):
    await ctx.send(random.choice(emojiler))

@bot.command()
async def meme(ctx):
    liste = [
        "images/meme1.jpg","images/meme2.jpg","images/meme3.jpg",
        "images/meme4.jpg","images/meme5.jpg","images/meme6.jpg","images/meme7.jpg"
    ]
    yol = random.choice(liste)
    try:
        with open(yol, "rb") as f:
            await ctx.send(file=discord.File(f, filename=os.path.basename(yol)))
    except FileNotFoundError:
        await ctx.send("Görsel dosyası bulunamadı. (images klasörü var mı?)")

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = res.json()
    return data['url']

@bot.command(name='duck')
async def duck(ctx):
    try:
        image_url = get_duck_image_url()
        await ctx.send(image_url)
    except Exception as e:
        await ctx.send(f"Ördek getirirken hata oluştu: {e}")

@bot.command()
async def kasa_oyunu(ctx):
    global event1
    if not event1:
        event1 = True
        await ctx.send(
            "🎉 KASA OYUNU BAŞLADI! 🎉\n"
            "3 kasa var 🔒🔒🔒\n"
            "Herhangi birini seçmek için $kasa_sec 1, 2 veya 3 yazın!"
        )
    else:
        await ctx.send("Zaten aktif bir oyun var. Önce onu bitirelim 🙂")

@bot.command()
async def kasa_sec(ctx, secilen: int = None):
    global event1
    if not event1:
        await ctx.send("Aktif bir oyun yok. $kasa_oyunu ile başlatın.")
        return

    if secilen is None:
        await ctx.send("Lütfen $kasa_sec 1, 2 veya 3 yazın.")
        return

    if secilen not in (1, 2, 3):
        await ctx.send("Sadece 1, 2 veya 3 seçebilirsiniz.")
        return

    dogru_secenek = random.randint(1, 3)

    # Oyun biter
    event1 = False

    if secilen == dogru_secenek:
        await ctx.send("🎊 Doğru kasayı buldunuz! 💎")
    else:
        await ctx.send(f"Seçtiğiniz kasa boştu. Doğru kasa *{dogru_secenek}* idi.")

    # Sayaç artır
    sayi = _kasa_sayisini_oku() + 1
    _kasa_sayisini_yaz(sayi)

@bot.command()
async def acilan_kasa_sayisi(ctx):
    sayi = _kasa_sayisini_oku()
    await ctx.send(f"Toplam açılan kasa sayısı: {sayi}")

# --- Çalıştır ---
if __name__ == "_main_":
    if not TOKEN:
        raise RuntimeError(
            "DISCORD_TOKEN bulunamadı. Lütfen TOKEN'ı .env'e veya ortama koyun ya da koda düz yazın."
        )

bot.run("")
