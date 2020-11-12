import telebot
from telebot import types
bot = telebot.TeleBot("TOKEN", parse_mode=None) 
from PIL import Image
import os
"""
Developed By Mahmoud Alarby
	@Seth0x41 --> Facebook
	https://t.me/M7moudAl3rby --> Telegram

"""
@bot.message_handler(commands=['start'])
def startMessage(message):
    bot.send_message(chat_id=message.chat.id,text= """
Start message
""")


## Mathematics and computer science department
subject = os.path.dirname(os.path.abspath(__file__))
@bot.message_handler(commands=['mathandcs'])
def selectSubject(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='تفاضل وتكامل', callback_data="Calculus"))
    markup.add(telebot.types.InlineKeyboardButton(text='معادلات تفاضلية عادية', callback_data="OrdinaryDifferentialEquations"))
    markup.add(telebot.types.InlineKeyboardButton(text='هندسة فراغية', callback_data="StaticEngineering"))
    markup.add(telebot.types.InlineKeyboardButton(text='رياضيات متقطعة', callback_data="DiscreteMathematics"))
    markup.add(telebot.types.InlineKeyboardButton(text='بناء حاسب', callback_data="ComputerArchitecture"))
    markup.add(telebot.types.InlineKeyboardButton(text='برمجة هيكلية', callback_data="StructuredProgramming"))
    bot.send_message(message.chat.id, text="هتذاكر إيه النهارده ؟", reply_markup=markup)
	
 ## Handle and create dynamic buttons 

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global subject
    subject = call.data
    path=os.path.dirname(os.path.abspath(__file__))+"/"+call.data
    lectures=types.ReplyKeyboardMarkup(resize_keyboard=True)
    if os.path.exists(path) == True:
        for filename in sorted(os.listdir(path)):
            if filename != "bot.py":
                lectures.add(telebot.types.KeyboardButton(text=filename))
    bot.send_message(call.message.chat.id,"تمام، اى محاضرة ؟ ",reply_markup=lectures)
    bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id)

## handle call back and message text fuction and send photos

@bot.message_handler(content_types=['text'])
def processing(message):
    if message.text.isdigit():
        url =  subject+"/"+message.text
        if os.path.exists(url) == True:
            for lecture in sorted(os.listdir(url)):
                url =  subject+"/"+message.text+"/"+lecture 

                if lecture.endswith(".jpg") or lecture.endswith(".png"):
                    photo = open(url, 'rb')
                    bot.send_photo(message.chat.id, photo)
                elif lecture.endswith(".pdf"):
                    doc = open(url, 'rb')
                    bot.send_document(message.chat.id, doc)
                    bot.send_document(message.chat.id, "FILEID")
                elif lecture.endswith(".txt"):
                    with open(url,'rb') as f:
                        data = f.read()
                        bot.send_message(chat_id=message.chat.id,text=data)
                        f.close()
                else:
                    print("Something wrong!")
        else:
            bot.send_message(message.chat.id,text="المحاضرة لسه متوفرتش")
    else:
        bot.send_message(message.chat.id,text="لو سمحت إختار من القايمة إلى عندك")
bot.polling()
