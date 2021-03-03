import telebot
import coc
from decouple import config

import bot_message

bot = telebot.TeleBot(config('BOTAPI',cast=str))

client = coc.login(config('EMAIL', cast=str), config('PASS', cast=str))

#Bot related functions
@bot.message_handler(commands=['start'])
def handle_command(message):

    if message.chat.type == "private":

        keyboard = telebot.types.InlineKeyboardMarkup()
        help_button = telebot.types.InlineKeyboardButton('Help', callback_data='help')
        Contact_button = telebot.types.InlineKeyboardButton('Contact', url='https://t.me/joinchat/VW7QJ1LJ_PXDFEpr')
        keyboard.add(help_button, Contact_button)

        bot.send_message(message.chat.id, bot_message.start_message, reply_markup=keyboard, parse_mode='HTML')
    
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

        bot.edit_message_text(bot_message.help_message, call.message.chat.id, call.message.id, reply_markup=keyboard, parse_mode='HTML')

    elif call.data == 'clans':

        keyboard = telebot.types.InlineKeyboardMarkup()
        back_button = telebot.types.InlineKeyboardButton('Back', callback_data='help',)
        keyboard.add(back_button)

        bot.edit_message_text(bot_message.clan_button_message, call.message.chat.id, call.message.id, reply_markup=keyboard, parse_mode='HTML')
    
    elif call.data == 'players':

        keyboard = telebot.types.InlineKeyboardMarkup()
        back_button = telebot.types.InlineKeyboardButton('Back', callback_data='help')
        keyboard.add(back_button)

        bot.edit_message_text(bot_message.player_button_message, call.message.chat.id, call.message.id, reply_markup=keyboard, parse_mode='HTML')


#Clans related functions
@bot.message_handler(commands=['getClan'])
def handle_command(message):

    async def getInfo():

        try:
            clan_tag = message.text.split()[1]
            clan = await client.get_clan(clan_tag)

            bot.send_photo(message.chat.id, clan.badge.url, bot_message.clan_message.format(clan.name, clan.level, clan.share_link), message.message_id)

        except IndexError:
            bot.reply_to(message, f"Incomplete Command! Make sure to put correct id with '#' start of it.")

        except coc.errors.NotFound:
            bot.reply_to(message, f"Not Found! Make sure to put correct id with '#' start of it.")
        
        except Exception:
            pass
    
    client.loop.run_until_complete(getInfo())


@bot.message_handler(commands=['getClanDetails'])
def handle_command(message):

    async def getInfo():

        try:
            clan_tag = message.text.split()[1]
            clan = await client.get_clan(clan_tag)

            bot.reply_to(message, bot_message.clan_details_message.format(
                clan.name,
                clan.level,
                clan.description,
                clan.location,
                clan.points,
                clan.versus_points,
                clan.type,
                clan.required_trophies,
                clan.member_count,
                clan.war_league,
                clan.war_frequency,
                clan.war_wins,
                clan.war_losses,
                clan.war_win_streak,
            ))

        except IndexError:
            bot.reply_to(message, f"Incomplete Command! Make sure to put correct id with '#' start of it.")

        except coc.errors.NotFound:
            bot.reply_to(message, f"Not Found! Make sure to put correct id with '#' start of it.")
        
        except Exception:
            pass
    
    client.loop.run_until_complete(getInfo())


bot.polling()

while True:
    pass