import gtts
import telebot
import os
from textblob import TextBlob

#ваше токен от телеграм бота
API_TOKEN = 'TOKEN'
bot = telebot.TeleBot(token = API_TOKEN)

@bot.message_handler(commands=['start'])
def handler_start(message):
    bot.send_message(message.chat.id,'Привет, я буду делать годноту\nВыбери подходящий вариант для тебя.')

@bot.message_handler(content_types=["text"])
def handle_reply_text(message):
    if len(message.text) < 3:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "Попробуй ка больше 3 символов, а!!")
        return 0
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
        return 0
    except Exception as e:
        bot.reply_to(message, e)

#создаем имя файла
def create_name(textspeech):
    # проверка на длину имени
    if len(textspeech) > 23:
        # конкатинация первых 20 символом и троеточия
        return textspeech[0:20] + '...'
    else:
        return textspeech

#создаем патч к нашему голосовому
def create_patch(name):
    return name+'.mp3'
#определяем язык
def detect_lang(textspeech):
    b = TextBlob(textspeech)
    lang = b.detect_language()
    return lang
#конвертируем текст в голос
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
#проверка на фото, возможно будет распознавание
@bot.message_handler(content_types=["photo"])
def handle_reply_photo(message):
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "Не торопись, скоро будет\
    распознавание и по картинке!")
if __name__ == '__main__':
    bot.polling(none_stop=True)