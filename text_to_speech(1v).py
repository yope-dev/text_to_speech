#import start
import gtts
import telebot
import os
from textblob import TextBlob
from telebot import types
#import end
API_TOKEN = 'TOKEN'
bot = telebot.TeleBot(token = API_TOKEN)
@bot.message_handler(commands=['start'])
def handler_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,one_time_keyboard = True)
    b1 = types.KeyboardButton('Быстрый способ')
    b2 = types.KeyboardButton('Продвинутый способ')
    markup.add(b1, b2)
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id,'Привет, я буду делать годноту\nВыбери подходящий вариант для тебя.', reply_markup=markup)

@bot.message_handler(commands=['instagram'])
def send_inst(message):
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id,'https://www.instagram.com/pp_andr')

@bot.message_handler(content_types=["text"])
def handle_reply_text(message):
    if check_users_in_bd(message) == 0:
        return 0
    d = []
    # разбиваем по символу
    res1 = message.text.split(" ")
    for val in res1:
    	#срезаю пробелы
    	val = val.strip()
    	#формирую новый массив
    	d.append(val)
    get_message_bot = message.text.strip().lower()
    elif get_message_bot == "быстрый способ":
        msg = bot.reply_to(message, "Введи любой текст:")
        return bot.register_next_step_handler(msg, fast)
    elif get_message_bot == "продвинутый способ":
        msg = bot.reply_to(message, "Введи любой текст:")
        return bot.register_next_step_handler(msg, long_method)
    if len(message.text) < 3:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "Попробуй ка больше 3 символов, а!!")
        return 0
def fast(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")
        textspeech = message.text
        # определяем какой язык
        l = detect_lang(textspeech)
         # задаем имя файлу
        name = create_name(textspeech)
        # расположение файла
        patch = create_patch(name)
        bot.send_chat_action(message.chat.id, "record_audio")
        # преобразование текста в голос
        c = text_to_speech(message,textspeech,l,patch)
        if c == 0:
            return 0
        bot.send_chat_action(message.chat.id, "upload_audio")
        audio = open(patch, 'rb')
        # отправка аудио
        bot.send_audio(message.chat.id, audio, title = name,
        performer = "Speech Bot",caption = "@spee_ch_bot")
        # удаляем файл, что-бы не засорять место
        os.remove(patch)
        keyb(message)
        return 0
    except Exception as e:
        bot.reply_to(message, e)
def long_method(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")
        global text_speech
        text_speech = message.text
        # определяем какой язык
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard = True)
        b1 = types.KeyboardButton('Ukrainian')
        b2 = types.KeyboardButton('Russian')
        b3 = types.KeyboardButton('English')
        b4 = types.KeyboardButton('French')
        b5 = types.KeyboardButton('German')
        b6 = types.KeyboardButton('Auto-detect')
        markup.add(b1, b2,b3,b4,b5,b6)
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id,'Выбери язык:', reply_markup=markup)
        bot.register_next_step_handler(message, select_language)
    except Exception as e:
        bot.reply_to(message, e)
def select_language(message):
    try:
        global l
        global text_speech
        if message.text.strip().lower() == 'ukrainian':
            l = 'uk'
        elif message.text.strip().lower() == 'russian':
            l = 'ru'
        elif message.text.strip().lower() == 'english':
            l = 'en'
        elif message.text.strip().lower() == 'french':
            l = 'fr'
        elif message.text.strip().lower() == 'german':
            l = 'de'
        else:
            l = detect_lang(text_speech)
        bot.send_chat_action(message.chat.id, "record_audio")
        bot.send_message(message.chat.id,'Введите название:')
        bot.register_next_step_handler(message, select_name)
    except Exception as e:
        bot.reply_to(message, e)
def select_name(message):
    try:
        name = message.text
        global text_speech
        global l
        # расположение файла
        patch = create_patch(name)
        # преобразование текста в голос
        c = text_to_speech(message,text_speech,l,patch)
        if c == 0:
            return 0
        bot.send_chat_action(message.chat.id, "upload_audio")
        audio = open(patch, 'rb')
        # отправка аудио
        bot.send_audio(message.chat.id, audio, title = name,
        performer = "Speech Bot",caption = "@spee_ch_bot")
        # удаляем файл, что-бы не засорять место
        os.remove(patch)
        keyb(message)
        return 0
    except Exception as e:
        bot.reply_to(message, e)
def create_name(textspeech):
    # проверка на длину имени
    if len(textspeech) > 23:
        # конкатинация первых 20 символом и троеточия
        return textspeech[0:20] + '...'
    else:
        return textspeech

def create_patch(name):
    return name+'.mp3'

def detect_lang(textspeech):
    b = TextBlob(textspeech)
    lang = b.detect_language()
    return lang
def text_to_speech(message,text, l,patch):
    try:
        tts = gtts.gTTS(text,lang=l,lang_check=False)
        tts.save(patch)
        return 1
    except:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "На данный момент язык "
        +l+" недоступен.")
        return 0
def keyb(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1,one_time_keyboard = True)
    b1 = types.KeyboardButton('Быстрый способ')
    b2 = types.KeyboardButton('Продвинутый способ')
    markup.add(b1, b2)
    bot.send_message(message.chat.id, "Продолжим?",reply_markup=markup)

@bot.message_handler(content_types=["photo"])
def handle_reply_photo(message):
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "Не торопись, скоро будет\
    распознавание и по картинке!")

if __name__ == '__main__':
    bot.polling(none_stop=True)