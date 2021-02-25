import telebot
import coc
from decouple import config


bot = telebot.TeleBot(config('BOTAPI',cast=str))

client = coc.login('kooolme444@gmail.com', '8299048747@love')

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
        bot.send_message(message.chat.id, f'''
I am Clash Bot which can used to fetch Players and Clan data of Clash of Clans!

Use /help command to get list of commands.''')
    
    else:   #For group chat
        bot.reply_to(message, f"I am up!")


@bot.message_handler(commands=['help'])
def handle_command(message):

    if message.chat.type == "private":
        bot.send_message(message.chat.id, f'''
Here is all the commands available yet - 

/getPlayerBh #<Player Tag> - To get Bh Level of a player
''')
    
    else:   #For group chat
        bot.reply_to(message, f"I'm kinda shy, DM for all info!")


bot.polling()

while True:
    pass