import os

import telebot
import schedule
from gtts import gTTS

from parser import WordParser

TOKEN = os.environ.get("BOT_TOKEN")


bot = telebot.TeleBot(TOKEN)
word = WordParser()
spam = False


def send_information(message):
    bot.send_message(message.chat.id, word.word.word)
    bot.send_message(message.chat.id, f"Definition - {word.word.description}")


@bot.message_handler(commands=["start"])
def start(message):
    global spam
    spam = True
    marcup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    get = telebot.types.KeyboardButton("/Give me a new word")
    transcription = telebot.types.KeyboardButton("/Transcription")
    synonyms = telebot.types.KeyboardButton("/What about synonyms?")
    pronounce = telebot.types.KeyboardButton("/How to pronounce it?")

    marcup.add(get, transcription, synonyms, pronounce)
    bot.send_message(message.chat.id, f"Helo {message.from_user.first_name}")
    bot.send_message(message.chat.id, "What do you need?", reply_markup=marcup)

    schedule.every().day.at("12:00").do(get_random_word, message)

    while spam:
        schedule.run_pending()


@bot.message_handler(commands=["get", "Give"])
def get_random_word(message):
    global word
    word = WordParser()
    send_information(message)


@bot.message_handler(commands=["repeat", "Repeat"])
def repeat(message):
    send_information(message)


@bot.message_handler(commands=["transcription", "Transcription"])
def get_transcription(message):
    transcription = word.word.pronounce
    if transcription:
        bot.send_message(message.chat.id, word.word.pronounce)
    else:
        bot.send_message(message.chat.id, "have not idea👎")


@bot.message_handler(commands=["How", "voice"])
def voice_pronounce(message):
    tts = gTTS(word.word.word)
    tts.save("audio/audio.mp3")
    with open("audio/audio.mp3", "rb") as audio:
        bot.send_voice(message.chat.id, audio)


@bot.message_handler(commands=["synonyms", "What"])
def get_synonyms(message):
    synonyms = word.word.synonyms
    if synonyms:
        bot.send_message(message.chat.id, f"Synonyms to {word.word.word} is:")
        for i in synonyms:
            bot.send_message(message.chat.id, i)
    else:
        bot.send_message(message.chat.id, "I don't know😞")


@bot.message_handler(commands=["stop"])
def stop_spamming(message):
    global spam
    spam = False
    bot.send_message(message.chat.id, "Good bye")
    bot.send_message(message.chat.id, "👋")


@bot.message_handler(content_types=["text"])
def get_certain_word(message):
    message_text = message.text.strip("/")
    if len(message_text.split()) > 1 or not message_text.isalpha():
        bot.send_message(message.chat.id, "Please send me one word😉")
    else:
        global word
        word = WordParser(message_text)
        send_information(message)
    print(message_text)


bot.polling(non_stop=True)
