import os
from threading import Thread


import telebot
import schedule
from gtts import gTTS

from parser import WordParser
from chats.chats import Chat

TOKEN = os.environ.get("TEST_TOKEN") or os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
chats = set(Chat.get_chats())


def send_information(chat: Chat):
    bot.send_message(chat.id, chat.word.word.word)
    bot.send_message(chat.id, f"Definition - {chat.word.word.description}")


@bot.message_handler(commands=["start"])
def start(message):
    chat = Chat(message)
    chat.spam = True
    chats.add(chat)
    chat.save_chats()

    marcup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    get = telebot.types.KeyboardButton("/Give me a new word")
    transcription = telebot.types.KeyboardButton("/Transcription")
    synonyms = telebot.types.KeyboardButton("/What about synonyms?")
    pronounce = telebot.types.KeyboardButton("/How to pronounce it?")

    marcup.add(get, transcription, synonyms, pronounce)
    bot.send_message(chat.id, f"Helo {message.from_user.first_name}")
    bot.send_message(chat.id, "What do you need?", reply_markup=marcup)


@bot.message_handler(commands=["get", "Give"])
def get_random_word(message):
    chat = Chat.get_chat(message)
    chat.word = WordParser()
    send_information(chat)
    chat.save_chats()


@bot.message_handler(commands=["repeat", "Repeat"])
def repeat(message):
    chat = Chat.get_chat(message)
    send_information(chat)


@bot.message_handler(commands=["transcription", "Transcription"])
def get_transcription(message):
    chat = Chat.get_chat(message)
    transcription = chat.word.word.pronounce
    if transcription:
        bot.send_message(chat.id, chat.word.word.pronounce)
    else:
        bot.send_message(chat.id, "have not idea👎")


@bot.message_handler(commands=["How", "voice"])
def voice_pronounce(message):
    chat = Chat.get_chat(message)
    tts = gTTS(chat.word.word.word)
    tts.save("audio/audio.mp3")
    with open("audio/audio.mp3", "rb") as audio:
        bot.send_voice(chat.id, audio)


@bot.message_handler(commands=["read"])
def voice_description(message):
    chat = Chat.get_chat(message)
    tts = gTTS(chat.word.word.word)
    tts.save("audio/description.mp3")

    with open("audio/description.mp3", "rb") as audio:
        bot.send_voice(message.chat.id, audio)


@bot.message_handler(commands=["synonyms", "What"])
def get_synonyms(message):
    chat = Chat.get_chat(message)
    synonyms = chat.word.word.synonyms
    if synonyms:
        bot.send_message(chat.id, f"Synonyms to {chat.word.word.word} is:")
        for i in synonyms:
            bot.send_message(chat.id, i)
    else:
        bot.send_message(chat.id, "I don't know😞")


@bot.message_handler(commands=["stop"])
def stop_spamming(message):
    chat = Chat.get_chat(message)
    chat.spam = False
    bot.send_message(chat.id, "Good bye")
    bot.send_message(chat.id, "👋")


@bot.message_handler(content_types=["text"])
def get_certain_word(message):
    chat = Chat.get_chat(message)
    message_text = message.text.strip("/")
    if len(message_text.split()) > 1:
        bot.send_message(chat.id, "Please send me one word😉")
    else:
        chat.word = WordParser(message_text)
        send_information(chat)
    chat.save_chats()
    print(message_text)


def send_message_every_day():
    for chat in chats:
        if chat.spam:
            chat.word = WordParser()
            send_information(chat)


def scheduler():
    schedule.every().day.at("12:00").do(send_message_every_day)
    while True:
        schedule.run_pending()


Thread(target=scheduler, args=()).start()
bot.polling(non_stop=True)
