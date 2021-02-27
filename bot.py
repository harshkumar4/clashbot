import telebot
import coc
from decouple import config

from bot_message import start_message, help_message, clan_button_message, player_button_message

bot = telebot.TeleBot(config('BOTAPI',cast=str))

client = coc.login(config('EMAIL', cast=str), config('PASS', cast=str))

@bot.message_handler(commands=['getPlayerBh'])
def handle_command(message):

    async def getInfo():

        try:
            player_tag = message.text.split()[1]
            player = await client.get_player(player_tag)

            bot.reply_to(message, f"Your BH level is {player.builder_hall}.")

        except IndexError:
            bot.reply_to(message, f"Incomplete Command!, Make sure to put correct id with '#' start of it.")

        except coc.errors.NotFound:
            bot.reply_to(message, f"Not Found!, Make sure to put correct id with '#' start of it.")
        
        except Exception:
            pass
            
    client.loop.run_until_complete(getInfo())


@bot.message_handler(commands=['start'])
def handle_command(message):

    if message.chat.type == "private":

        keyboard = telebot.types.InlineKeyboardMarkup()
        help_button = telebot.types.InlineKeyboardButton('Help', callback_data='help')
        keyboard.add(help_button)
        bot.send_message(message.chat.id, start_message, reply_markup=keyboard, parse_mode='HTML')
    
    else:   #For group chat
        bot.reply_to(message, f"I am up!")


@bot.message_handler(commands=['help'])
def handle_command(message):

    if message.chat.type != "private":
        
        keyboard = telebot.types.InlineKeyboardMarkup()
        help_button = telebot.types.InlineKeyboardButton('Help', url='http://t.me/getclashbot')
        keyboard.add(help_button)

        bot.reply_to(message, f"I'm kinda shy, DM for all info!", reply_markup=keyboard, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    
    if call.data == 'help':

        keyboard = telebot.types.InlineKeyboardMarkup()
        clan_button = telebot.types.InlineKeyboardButton('Clans', callback_data='clans')
        player_button = telebot.types.InlineKeyboardButton('Players', callback_data='players')
        keyboard.add(clan_button, player_button)

        bot.edit_message_text(help_message, call.message.chat.id, call.message.id, reply_markup=keyboard, parse_mode='HTML')

    elif call.data == 'clans':

        keyboard = telebot.types.InlineKeyboardMarkup()
        back_button = telebot.types.InlineKeyboardButton('Back', callback_data='help',)
        keyboard.add(back_button)

        bot.edit_message_text(clan_button_message, call.message.chat.id, call.message.id, reply_markup=keyboard, parse_mode='HTML')
    
    elif call.data == 'players':

        keyboard = telebot.types.InlineKeyboardMarkup()
        back_button = telebot.types.InlineKeyboardButton('Back', callback_data='help')
        keyboard.add(back_button)

        bot.edit_message_text(player_button_message, call.message.chat.id, call.message.id, reply_markup=keyboard, parse_mode='HTML')


bot.polling()

while True:
    pass