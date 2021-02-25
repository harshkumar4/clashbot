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


@bot.message_handler(commands=['start', 'help'])
def handle_command(message):
    bot.reply_to(message, f'''I am Clash Bot and can used to fetch data related to Clash of Clans!
Here are some following commands available yet:-
    
/getPlayerBh #<Player Id> To get a player's BH level.''')


    
bot.polling()

while True:
    pass

# @bot.message_handler(func=lambda m:True)
# def handle_command(message):
#     print(getPlayerBh())
#     bot.reply_to(message, getPlayerBh)