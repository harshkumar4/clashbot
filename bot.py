import telebot
import coc
from decouple import config

bot = telebot.TeleBot(config('BOTAPI',cast=str))

client = coc.login('kooolme444@gmail.com', '8299048747@love')

@bot.message_handler(commands=['getPlayerBh'])
def handle_command(message):

    async def mainn():

        try:
            player_tag = message.text.split()[1]
            player = await client.get_player(player_tag)

            bot.reply_to(message, f"Your BH level is {player.builder_hall}.")

        except IndexError:
            bot.reply_to(message, f"Incomplete Command!")

        except Exception:
            pass
            
    client.loop.run_until_complete(mainn())
    
bot.polling()

while True:
    pass
client.close()

# @bot.message_handler(func=lambda m:True)
# def handle_command(message):
#     print(getPlayerBh())
#     bot.reply_to(message, getPlayerBh)
