import telebot
import random

bot = telebot.TeleBot(TOKEN) #token is hidden in the public code

@bot.message_handler(content_types=['text'])

def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Введите вашу фамилию: ")
        bot.register_next_step_handler(message, get_family_name)
    else:
        bot.send_message(message.from_user.id, 'Добрый день! Напишите /start, чтобы запустить бота')

def get_family_name(message):
    global family_name
    family_name = message.text
    bot.send_message(message.from_user.id, 'Введите ваше имя: ')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name
    name = message.text
    with open('linguists_list.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        f.close()
    with open('nicknames_table.txt', 'r', encoding='utf-8') as f:
        nickslines = f.read()
        f.close()
    names = text.splitlines()
    nickrows = nickslines.splitlines()
    existing = [nickrow.split('\t')[2] for nickrow in nickrows]
    possible_names = [name for name in names if name not in existing]
    if possible_names:
        nickname = random.choice(possible_names)
        with open('nicknames_table.txt', "a") as wr:
            wr.write(name)
            wr.write('\t')
            wr.write(family_name)
            wr.write('\t')
            wr.write(nickname)
            wr.write('\n')
            wr.close()
        resp = 'Ваш псевдоним: ' + nickname
        bot.send_message(message.from_user.id, resp)
    else:
        bot.send_message('Извините, синтаксисты закончились :( Если вы видите это сообщение, напишите Денису (он чего-то сломал)')

bot.polling(none_stop=True, interval=0)
