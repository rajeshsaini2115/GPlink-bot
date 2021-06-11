from os import environ
import datetime
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = 'e79d26ac675025e1bfd29c5e93415f33d95b007b'

bot = Client('gplink bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!** \n\nThis is **GPLinks URL Shorter Bot**. Just send me any big link and get short link.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Movie Channel', url='https://t.me/mrkpmovies')
                ],
                [
                    InlineKeyboardButton('Movie Request Group', url='https://t.me/mrkprequest')
                ]
            ]
        )
    )
    
    
@bot.on_message(filters.command('repo') & filters.private)
async def repo(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!** \n\nThis is **GPLinks URL Shorter Bot**. If you want to make your own GPLinks Bot than Contact Owner.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Owner', url='https://t.me/rajeshsaini2115'),
                    InlineKeyboardButton('Get API', url='https://gplinks.in/ref/yostartech')
                ],
                [
                    InlineKeyboardButton('Movie Request Group', url='https://t.me/mrkprequest')
                ]
            ]
        )
    )
    
    

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link)
        await message.reply(
            text=f"Here is your short link: {short_link}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Open Link', url=short_link)
                    ]
                ]
            ),
            quote=True
        )
        now = datetime.datetime.now()
        chat_id = environ.get('LOG_CHANNEL', -1001302061161)
        uname = f"[{message.from_user.first_name}](tg://openmessage?user_id={message.from_user.id})"
        await bot.send_message(chat_id, f"**#SHORTEN: \n\n@mrkpgplinkbot Shortened** {link} **to** {short_link} **for** {uname} **at** `{now}`", parse_mode="markdown", disable_web_page_preview=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = 'https://gplinks.in/api'
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]


bot.run()
