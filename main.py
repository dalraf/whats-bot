import re
from bot import wppbot

bot = wppbot('robozin')
#bot.treina('treino')
#bot.inicia('Capitalismo Opressor News')
bot.inicia('Fábio Assunção THE BOSS')
#bot.saudacao(['bot: Oi, sou um bot','bot: Bora conversar ?'])
ultimo_texto = ''
botname = 'Fábio Assunção:'



while True:

    texto = bot.escuta()

    if texto != ultimo_texto and not re.match(r'^' + botname, texto):

        ultimo_texto = texto
        texto = texto.replace('', '')
        texto = texto.lower()

        if texto == "erro":
            break
        else:
            bot.responde(texto,botname)