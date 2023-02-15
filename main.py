import os

import telebot

from parser import WordParser

TOKEN = os.environ.get("BOT_TOKEN")


bot = telebot.TeleBot(TOKEN)
word = WordParser()


def send_information(message):
    bot.send_message(message.chat.id, word.word.word)
    bot.send_message(message.chat.id, f"Definition - {word.word.description}")


@bot.message_handler(commands=["start"])
def start(message):
    marcup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    get = telebot.types.KeyboardButton("/Give me a new word")
    repeat_message = telebot.types.KeyboardButton("/Repeat please")
    transcription = telebot.types.KeyboardButton("/How to pronounce it")
    synonyms = telebot.types.KeyboardButton("/What about synonyms?")

    marcup.add(get, repeat_message, transcription, synonyms)
    bot.send_message(message.chat.id, f"Helo {message.from_user.first_name}")
    bot.send_message(message.chat.id, "What do you need?", reply_markup=marcup)


@bot.message_handler(commands=["get", "Give"])
def get_random_word(message):
    global word
    word = WordParser()
    send_information(message)


@bot.message_handler(commands=["repeat", "Repeat"])
def repeat(message):
    send_information(message)


@bot.message_handler(commands=["transcription", "How"])
def get_transcription(message):
    transcription = word.word.pronounce
    if transcription:
        bot.send_message(message.chat.id, word.word.pronounce)
    else:
        bot.send_message(message.chat.id, "have not idea👎")


@bot.message_handler(commands=["synonyms", "What"])
def get_synonyms(message):
    synonyms = word.word.synonyms
    if synonyms:
        bot.send_message(message.chat.id, f"Synonyms to {word.word.word} is:")
        for i in synonyms:
            bot.send_message(message.chat.id, i)
    else:
        bot.send_message(message.chat.id, "I don't know😞")


@bot.message_handler(content_types=["text"])
def get_certain_word(message):
    message_text = message.text.strip("/")
    print(message_text)
    global word
    word = WordParser(message_text)
    send_information(message)


bot.polling(non_stop=True)
