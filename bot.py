import os
import json
import telebot
import config #where my api key and bot token stores
import openai
from telebot import types

openai.api_key = config.api_key

bot = telebot.TeleBot(config.TOKEN)
global defaultEngine
defaultEngine = "text-davinci-001"

@bot.message_handler(commands=['start'])
def welcome(message):
    markup1 = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Davinci (recommend)", callback_data="dav")
    item2 = types.InlineKeyboardButton("Curie", callback_data="cur")
    markup1.add(item1, item2)

    msg = "Hello welcome to ChatGPT bot!\n\nChoose your search engine (You can always change it in /settings !)\n\nmade by vleo"

    bot.send_message(message.chat.id, msg, reply_markup=markup1)

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    msg = "Now you can use ChatGPT!\n\nWrite your message to it:"
    try:
        if call.message:
            global defaultEngine
            if call.data == "cur":
                defaultEngine = "text-curie-001"
                bot.send_message(call.message.chat.id, msg)
            elif call.data == "dav":
                defaultEngine = "text-davinci-001"
                bot.send_message(call.message.chat.id, msg)

    except Exception as e:
        print(repr(e))

@bot.message_handler(content_types=['text'])
def lol(message):
    prompt = message.text
    data = openai.Completion.create(engine=defaultEngine, prompt=prompt, max_tokens=200)
    msg = data["choices"][0]["text"]
    bot.send_message(message.chat.id, msg)

#RUN
bot.polling(none_stop=True)
