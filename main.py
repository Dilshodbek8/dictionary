import telebot
import requests
from googletrans import Translator

TOKEN = '5085514712:AAGmvBfjGCmeWii_mf-2aRyi2K8Dd_gi7aY'
URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/{}'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'Assalom aleykum qaysi so\'zni izlayabsiz? \n'
                                           'Здравствуйте, какое слово вы ищете?  \n'
                                           'Hello, what word are you looking for? \n\n'
                                           'Example: Person')
def get_syn_ant(list, name):
    if list:
        name = ''
        for i in list:
            name += f', {i} '
    else:
        name = 'not found'
    return name
#
# def get_audio(message, name):
#     r = requests.get(f'http:{message}')
#     with open(f'media/{name}.mp3', 'wb') as f:
#         f.write(r.content)
#

# def send_audio(message, url, name, body):
#     get_audio(url, name)
#     bot.send_chat_action(message.from_user.id, "record_voice")
#     with open(f'media/{name}.mp3', 'rb') as f:
#         music = f.read()
#     bot.send_audio(message.from_user.id, audio=music, caption=body)


def get_translation(word, lang):
    try:
        translator = Translator()
        translation = translator.translate(f"{word}", dest=f'{lang}')
        return translation.text
    except:
        return 'not found'


@bot.message_handler(func=lambda m: True)
def translate(message):
    try:
        r = requests.get(URL.format(message.text)).json()[0]
        data = r['meanings'][0]['definitions'][0]
        phonetics = r['phonetics'][0]['text']
        try:
            example = data['example']
        except:
            example = 'no examples'
        try:
            definition = data['definition']
        except:
            definition = 'no definitions'
        try:
            partOfSpeech = r['meanings'][0]['partOfSpeech']
        except:
            partOfSpeech = 'no partOfSpeech'
        synonyms = get_syn_ant(data['synonyms'], 'synonyms')
        antonyms = get_syn_ant(data['antonyms'], 'antonyms')
        uz = get_translation(message.text, 'uz')
        ru = get_translation(message.text, 'ru')
        # audio = r['phonetics'][0]['audio']
        text = f'🔎 word: {message.text} \n\n' \
               f'🔊 phonetics: {phonetics} \n\n' \
               f'📚 collocation: {partOfSpeech} \n\n' \
               f'🧑🏻‍🏫 definition  : {definition} \n\n' \
               f'🎯 example:  {example}\n\n ' \
               f'⚖️ synonyms: {synonyms} \n\n' \
               f'📈 antonyms: {antonyms} \n\n ' \
               f'🇺🇿 UZ: {uz} \n\n' \
               f'🇷🇺 RU: {ru} \n\n' \
               f'discover any words with: @ielts_dictionary_bot'
        # send_audio(message, audio, message.text, text, timeout=123)
        bot.send_message(message.from_user.id, text)
        bot.send_message(1576762539, f'{message.text}, \nuname={message.from_user.username} \nname={message.from_user.first_name} {message.from_user.id}')

    except Exception as e:
        bot.send_message(message.from_user.id, 'this word is not english or you wrote it wrong ')


bot.polling(none_stop=True)
